use anyhow::Result;
use shared_types::{AudioChunk, AudioConfig, AudioDeviceInfo};
use tokio::sync::mpsc;
use tokio::task::JoinHandle;
use tracing::info;

pub struct MacOSLoopback;

impl MacOSLoopback {
    pub fn new() -> Result<Self> {
        Ok(Self)
    }
}

impl crate::loopback::LoopbackCapture for MacOSLoopback {
    fn start(&mut self, _config: AudioConfig, _sender: mpsc::Sender<AudioChunk>) -> Result<JoinHandle<()>> {
        info!("macOS loopback requires BlackHole 2ch audio loopback driver installed.");
        let handle = tokio::spawn(async move {
            // macOS CoreAudio loopback loop
        });
        Ok(handle)
    }

    fn stop(&mut self) -> Result<()> {
        Ok(())
    }

    fn list_devices(&self) -> Result<Vec<AudioDeviceInfo>> {
        Ok(vec![AudioDeviceInfo {
            id: "blackhole".to_string(),
            name: "BlackHole 2ch (Virtual Loopback)".to_string(),
            is_default: true,
        }])
    }

    fn get_default_device(&self) -> Result<AudioDeviceInfo> {
        Ok(AudioDeviceInfo {
            id: "blackhole".to_string(),
            name: "BlackHole 2ch".to_string(),
            is_default: true,
        })
    }
}
