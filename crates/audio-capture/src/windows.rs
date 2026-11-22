use anyhow::{Context, Result};
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use cpal::{SampleFormat, StreamConfig};
use shared_types::{AudioChunk, AudioConfig, AudioDeviceInfo};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::time::{SystemTime, UNIX_EPOCH};
use tokio::sync::mpsc;
use tokio::task::JoinHandle;
use tracing::{error, info};

pub struct WindowsLoopback {
    host: cpal::Host,
    is_running: Arc<AtomicBool>,
}

impl WindowsLoopback {
    pub fn new() -> Result<Self> {
        let host = cpal::default_host();
        Ok(Self {
            host,
            is_running: Arc::new(AtomicBool::new(false)),
        })
    }
}

impl crate::loopback::LoopbackCapture for WindowsLoopback {
    fn start(&mut self, config: AudioConfig, sender: mpsc::Sender<AudioChunk>) -> Result<JoinHandle<()>> {
        self.is_running.store(true, Ordering::SeqCst);
        let is_running_clone = self.is_running.clone();

        // On Windows, default output device in loopback mode captures system audio
        let device = self
            .host
            .default_output_device()
            .context("No default audio output device found for Windows loopback capture")?;

        let supported_configs = device.supported_output_configs()?;
        let supported_config = supported_configs
            .filter(|c| c.sample_format() == SampleFormat::F32 || c.sample_format() == SampleFormat::I16)
            .next()
            .context("No supported audio stream config available")?
            .with_max_sample_rate();

        let sample_rate = supported_config.sample_rate().0;
        let channels = supported_config.channels();
        let stream_config: StreamConfig = supported_config.into();

        let handle = tokio::spawn(async move {
            let sender = sender.clone();
            let err_fn = |err| error!("An error occurred on system loopback stream: {}", err);

            let stream_result = match stream_config.sample_rate.0 {
                _ => device.build_input_stream(
                    &stream_config,
                    move |data: &[f32], _: &cpal::InputCallbackInfo| {
                        if !is_running_clone.load(Ordering::SeqCst) {
                            return;
                        }
                        // Mix multi-channel to mono if requested
                        let mono_data: Vec<f32> = if channels > 1 {
                            data.chunks(channels as usize)
                                .map(|frame| frame.iter().sum::<f32>() / (channels as f32))
                                .collect()
                        } else {
                            data.to_vec()
                        };

                        let now = SystemTime::now()
                            .duration_since(UNIX_EPOCH)
                            .unwrap_or_default()
                            .as_millis() as u64;

                        let chunk = AudioChunk {
                            data: mono_data,
                            timestamp_ms: now,
                            sample_rate,
                        };
                        let _ = sender.try_send(chunk);
                    },
                    err_fn,
                    None,
                ),
            };

            if let Ok(stream) = stream_result {
                if let Err(e) = stream.play() {
                    error!("Failed to play loopback stream: {}", e);
                    return;
                }
                while is_running_clone.load(Ordering::SeqCst) {
                    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
                }
            } else if let Err(e) = stream_result {
                error!("Failed to build Windows loopback stream: {}", e);
            }
        });

        info!("Windows system audio loopback capture started");
        Ok(handle)
    }

    fn stop(&mut self) -> Result<()> {
        self.is_running.store(false, Ordering::SeqCst);
        info!("Windows system audio loopback capture stopped");
        Ok(())
    }

    fn list_devices(&self) -> Result<Vec<AudioDeviceInfo>> {
        let mut devices = Vec::new();
        let default_name = self
            .host
            .default_output_device()
            .and_then(|d| d.name().ok())
            .unwrap_or_default();

        for (idx, device) in self.host.output_devices()?.enumerate() {
            let name = device.name().unwrap_or_else(|_| format!("Audio Device {}", idx));
            let is_default = name == default_name;
            devices.push(AudioDeviceInfo {
                id: format!("device-{}", idx),
                name,
                is_default,
            });
        }
        Ok(devices)
    }

    fn get_default_device(&self) -> Result<AudioDeviceInfo> {
        let device = self
            .host
            .default_output_device()
            .context("No default output device available")?;
        let name = device.name().unwrap_or_else(|_| "Default Audio Device".to_string());
        Ok(AudioDeviceInfo {
            id: "default".to_string(),
            name,
            is_default: true,
        })
    }
}
