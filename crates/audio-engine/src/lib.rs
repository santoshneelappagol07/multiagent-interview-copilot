pub mod config;
pub mod pipeline;

use anyhow::Result;
use config::AudioEngineConfig;
use pipeline::AudioPipeline;
use shared_types::AudioDeviceInfo;
use std::sync::Arc;
use tokio::sync::Mutex;
use tracing::info;

pub struct AudioEngine {
    config: AudioEngineConfig,
    pipeline: Arc<Mutex<Option<AudioPipeline>>>,
}

impl AudioEngine {
    pub fn new(config: AudioEngineConfig) -> Self {
        Self {
            config,
            pipeline: Arc::new(Mutex::new(None)),
        }
    }

    pub async fn start(&self) -> Result<()> {
        let mut pipe_guard = self.pipeline.lock().await;
        if pipe_guard.is_some() {
            info!("Audio engine is already running");
            return Ok(());
        }

        let mut pipeline = AudioPipeline::new(self.config.clone())?;
        pipeline.start().await?;
        *pipe_guard = Some(pipeline);

        info!("Audio engine successfully started");
        Ok(())
    }

    pub async fn stop(&self) -> Result<()> {
        let mut pipe_guard = self.pipeline.lock().await;
        if let Some(mut pipeline) = pipe_guard.take() {
            pipeline.stop().await?;
            info!("Audio engine successfully stopped");
        }
        Ok(())
    }

    pub async fn is_running(&self) -> bool {
        self.pipeline.lock().await.is_some()
    }

    pub async fn list_devices(&self) -> Result<Vec<AudioDeviceInfo>> {
        let capture = audio_capture::SystemAudioCapture::new(self.config.audio.clone())?;
        capture.list_devices()
    }
}
