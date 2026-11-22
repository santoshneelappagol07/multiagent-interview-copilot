mod audio;
mod commands;
mod error;
mod sidecar;
mod state;

use audio_engine::config::AudioEngineConfig;
use audio_engine::AudioEngine;
use state::AppState;
use tracing::info;

fn main() {
    tracing_subscriber::fmt::init();
    info!("Starting AI Voice Copilot Desktop Shell (Tauri 2)");

    let audio_config = AudioEngineConfig::default();
    let audio_engine = AudioEngine::new(audio_config);
    let app_state = AppState::new(audio_engine);

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .manage(app_state)
        .invoke_handler(tauri::generate_handler![
            commands::start_audio_capture,
            commands::stop_audio_capture,
            commands::get_audio_status,
            commands::list_audio_devices,
            commands::start_backend,
            commands::stop_backend,
            commands::get_backend_status,
            commands::get_app_config,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
