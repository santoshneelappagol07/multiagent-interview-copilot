use audio_engine::AudioEngine;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use tokio::process::Child;
use tokio::sync::Mutex;

pub struct AppState {
    pub audio_engine: Arc<AudioEngine>,
    pub is_capturing: Arc<AtomicBool>,
    pub backend_process: Arc<Mutex<Option<Child>>>,
}

impl AppState {
    pub fn new(audio_engine: AudioEngine) -> Self {
        Self {
            audio_engine: Arc::new(audio_engine),
            is_capturing: Arc::new(AtomicBool::new(false)),
            backend_process: Arc::new(Mutex::new(None)),
        }
    }

    pub fn set_capturing(&self, capturing: bool) {
        self.is_capturing.store(capturing, Ordering::SeqCst);
    }

    pub fn get_capturing(&self) -> bool {
        self.is_capturing.load(Ordering::SeqCst)
    }
}
