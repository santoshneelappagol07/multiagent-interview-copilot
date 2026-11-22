use anyhow::Result;
use shared_types::{AudioChunk, AudioConfig, AudioDeviceInfo};
use tokio::sync::mpsc;
use tokio::task::JoinHandle;

pub trait LoopbackCapture: Send + Sync {
    fn start(&mut self, config: AudioConfig, sender: mpsc::Sender<AudioChunk>) -> Result<JoinHandle<()>>;
    fn stop(&mut self) -> Result<()>;
    fn list_devices(&self) -> Result<Vec<AudioDeviceInfo>>;
    fn get_default_device(&self) -> Result<AudioDeviceInfo>;
}

pub fn create_loopback() -> Result<Box<dyn LoopbackCapture>> {
    #[cfg(target_os = "windows")]
    {
        Ok(Box::new(crate::windows::WindowsLoopback::new()?))
    }
    #[cfg(target_os = "macos")]
    {
        Ok(Box::new(crate::macos::MacOSLoopback::new()?))
    }
    #[cfg(not(any(target_os = "windows", target_os = "macos")))]
    {
        anyhow::bail!("Unsupported platform for system audio loopback capture")
    }
}
