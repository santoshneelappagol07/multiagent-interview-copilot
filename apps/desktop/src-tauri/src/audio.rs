use crate::error::DesktopError;
use audio_engine::AudioEngine;
use shared_types::AudioDeviceInfo;

pub async fn start_capture(engine: &AudioEngine) -> Result<(), DesktopError> {
    engine
        .start()
        .await
        .map_err(|e| DesktopError::Audio(e.to_string()))
}

pub async fn stop_capture(engine: &AudioEngine) -> Result<(), DesktopError> {
    engine
        .stop()
        .await
        .map_err(|e| DesktopError::Audio(e.to_string()))
}

pub async fn list_audio_devices(engine: &AudioEngine) -> Result<Vec<AudioDeviceInfo>, DesktopError> {
    engine
        .list_devices()
        .await
        .map_err(|e| DesktopError::Audio(e.to_string()))
}
