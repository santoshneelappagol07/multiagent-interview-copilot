pub mod loopback;
#[cfg(target_os = "macos")]
pub mod macos;
#[cfg(target_os = "windows")]
pub mod windows;

use anyhow::Result;
use loopback::{create_loopback, LoopbackCapture};
use shared_types::{AudioChunk, AudioConfig, AudioDeviceInfo};
use tokio::sync::mpsc;
use tokio::task::JoinHandle;

pub struct SystemAudioCapture {
    config: AudioConfig,
    inner: Box<dyn LoopbackCapture>,
}

impl SystemAudioCapture {
    pub fn new(config: AudioConfig) -> Result<Self> {
        let inner = create_loopback()?;
        Ok(Self { config, inner })
    }

    pub fn start_capture(&mut self, sender: mpsc::Sender<AudioChunk>) -> Result<JoinHandle<()>> {
        self.inner.start(self.config.clone(), sender)
    }

    pub fn stop(&mut self) -> Result<()> {
        self.inner.stop()
    }

    pub fn list_devices(&self) -> Result<Vec<AudioDeviceInfo>> {
        self.inner.list_devices()
    }

    pub fn get_default_device(&self) -> Result<AudioDeviceInfo> {
        self.inner.get_default_device()
    }
}
