use crate::state::AppState;
use serde::{Deserialize, Serialize};
use shared_types::AudioDeviceInfo;
use std::path::PathBuf;
use tauri::State;

#[derive(Serialize, Deserialize)]
pub struct AudioStatusResponse {
    pub is_capturing: bool,
    pub mode: String,
    pub sample_rate: u32,
}

#[derive(Serialize, Deserialize)]
pub struct AppConfigResponse {
    pub backend_url: String,
    pub ws_url: String,
    pub stt_provider: String,
}

#[tauri::command]
pub async fn start_audio_capture(
    _device_id: Option<String>,
    state: State<'_, AppState>,
) -> Result<(), String> {
    crate::audio::start_capture(&state.audio_engine)
        .await
        .map_err(|e| e.to_string())?;
    state.set_capturing(true);
    Ok(())
}

#[tauri::command]
pub async fn stop_audio_capture(state: State<'_, AppState>) -> Result<(), String> {
    crate::audio::stop_capture(&state.audio_engine)
        .await
        .map_err(|e| e.to_string())?;
    state.set_capturing(false);
    Ok(())
}

#[tauri::command]
pub async fn get_audio_status(state: State<'_, AppState>) -> Result<AudioStatusResponse, String> {
    Ok(AudioStatusResponse {
        is_capturing: state.get_capturing(),
        mode: "System Audio Loopback (Interviewer)".to_string(),
        sample_rate: 16000,
    })
}

#[tauri::command]
pub async fn list_audio_devices(state: State<'_, AppState>) -> Result<Vec<AudioDeviceInfo>, String> {
    crate::audio::list_audio_devices(&state.audio_engine)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn start_backend(state: State<'_, AppState>) -> Result<(), String> {
    let sidecar = crate::sidecar::SidecarManager::new(state.backend_process.clone());
    let current_dir = std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
    sidecar
        .start_backend(current_dir)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn stop_backend(state: State<'_, AppState>) -> Result<(), String> {
    let sidecar = crate::sidecar::SidecarManager::new(state.backend_process.clone());
    sidecar.stop_backend().await.map_err(|e| e.to_string())
}

#[tauri::command]
pub async fn get_backend_status(state: State<'_, AppState>) -> Result<bool, String> {
    let guard = state.backend_process.lock().await;
    Ok(guard.is_some())
}

#[tauri::command]
pub async fn get_app_config() -> Result<AppConfigResponse, String> {
    Ok(AppConfigResponse {
        backend_url: "http://127.0.0.1:8000".to_string(),
        ws_url: "ws://127.0.0.1:8000/ws".to_string(),
        stt_provider: "Whisper (System Audio Loopback)".to_string(),
    })
}
