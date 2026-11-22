pub mod provider;
pub mod whisper;

use anyhow::Result;
use provider::SttEngine;
use shared_types::{AudioChunk, SttProvider, TranscriptionResult};

#[derive(Debug, Clone)]
pub struct SttConfig {
    pub provider: SttProvider,
    pub model_path: String,
    pub language: String,
    pub device: String,
}

impl Default for SttConfig {
    fn default() -> Self {
        Self {
            provider: SttProvider::WhisperLocal,
            model_path: "models/ggml-base.en.bin".to_string(),
            language: "en".to_string(),
            device: "cpu".to_string(),
        }
    }
}

pub struct SttEngineFactory;

impl SttEngineFactory {
    pub fn create(config: SttConfig) -> Result<Box<dyn SttEngine>> {
        match config.provider {
            SttProvider::WhisperLocal => Ok(Box::new(whisper::WhisperStt::new(config)?)),
            _ => Ok(Box::new(whisper::WhisperStt::new(config)?)),
        }
    }
}
