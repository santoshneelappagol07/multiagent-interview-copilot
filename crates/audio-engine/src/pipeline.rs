use crate::config::AudioEngineConfig;
use anyhow::Result;
use audio_capture::SystemAudioCapture;
use audio_processing::AudioProcessor;
use shared_types::AudioChunk;
use std::net::SocketAddr;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use stt_engine::{provider::SttEngine, SttEngineFactory};
use tokio::sync::{broadcast, mpsc};
use tokio::task::JoinHandle;
use tracing::{error, info};
use vad_engine::SpeechSegmenter;

pub struct AudioPipeline {
    config: AudioEngineConfig,
    capture: SystemAudioCapture,
    is_running: Arc<AtomicBool>,
    tasks: Vec<JoinHandle<()>>,
}

impl AudioPipeline {
    pub fn new(config: AudioEngineConfig) -> Result<Self> {
        let capture = SystemAudioCapture::new(config.audio.clone())?;
        Ok(Self {
            config,
            capture,
            is_running: Arc::new(AtomicBool::new(false)),
            tasks: Vec::new(),
        })
    }

    pub async fn start(&mut self) -> Result<()> {
        self.is_running.store(true, Ordering::SeqCst);
        let is_running = self.is_running.clone();

        // Channels
        let (raw_tx, mut raw_rx) = mpsc::channel::<AudioChunk>(100);
        let (transcription_tx, _) = broadcast::channel(100);

        // Start gRPC server
        let grpc_addr: SocketAddr = format!("127.0.0.1:{}", self.config.grpc_port).parse()?;
        let grpc_tx = transcription_tx.clone();
        let grpc_handle = tokio::spawn(async move {
            if let Err(e) = streaming::start_grpc_server(grpc_addr, grpc_tx).await {
                error!("gRPC streaming server error: {}", e);
            }
        });
        self.tasks.push(grpc_handle);

        // Start system audio loopback capture
        let capture_handle = self.capture.start_capture(raw_tx)?;
        self.tasks.push(capture_handle);

        // Processing + VAD + STT Task
        let target_rate = self.config.audio.sample_rate;
        let vad_config = self.config.vad.clone();
        let stt_config = self.config.stt.clone();

        let processing_handle = tokio::spawn(async move {
            let mut processor = AudioProcessor::new(target_rate);
            let mut segmenter = SpeechSegmenter::new(vad_config);
            let mut stt: Box<dyn SttEngine> = match SttEngineFactory::create(stt_config) {
                Ok(engine) => engine,
                Err(e) => {
                    error!("Failed to initialize STT Engine: {}", e);
                    return;
                }
            };

            while is_running.load(Ordering::SeqCst) {
                if let Some(raw_chunk) = raw_rx.recv().await {
                    match processor.process(raw_chunk) {
                        Ok(processed) => {
                            if let Some(speech_chunk) = segmenter.process(&processed) {
                                match stt.transcribe_chunk(&speech_chunk) {
                                    Ok(result) => {
                                        if !result.text.trim().is_empty() {
                                            let proto_event = streaming::proto::TranscriptionEvent {
                                                text: result.text,
                                                is_partial: result.is_partial,
                                                timestamp_ms: result.timestamp_ms,
                                                confidence: result.confidence,
                                                language: result.language.unwrap_or_else(|| "en".to_string()),
                                            };
                                            let _ = transcription_tx.send(proto_event);
                                        }
                                    }
                                    Err(e) => {
                                        error!("STT transcription error: {}", e);
                                    }
                                }
                            }
                        }
                        Err(e) => {
                            error!("Audio processing error: {}", e);
                        }
                    }
                }
            }
        });

        self.tasks.push(processing_handle);
        info!("AudioPipeline started successfully");
        Ok(())
    }

    pub async fn stop(&mut self) -> Result<()> {
        self.is_running.store(false, Ordering::SeqCst);
        let _ = self.capture.stop();
        for task in self.tasks.drain(..) {
            task.abort();
        }
        info!("AudioPipeline stopped");
        Ok(())
    }
}
