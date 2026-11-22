use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioConfig {
    pub sample_rate: u32,
    pub channels: u16,
    pub buffer_ms: u32,
}

impl Default for AudioConfig {
    fn default() -> Self {
        Self {
            sample_rate: 16000,
            channels: 1,
            buffer_ms: 30,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioChunk {
    pub data: Vec<f32>,
    pub timestamp_ms: u64,
    pub sample_rate: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TranscriptionResult {
    pub text: String,
    pub is_partial: bool,
    pub timestamp_ms: u64,
    pub confidence: f32,
    pub language: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VadEvent {
    pub is_speech: bool,
    pub timestamp_ms: u64,
    pub confidence: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioDeviceInfo {
    pub id: String,
    pub name: String,
    pub is_default: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum SttProvider {
    WhisperLocal,
    WhisperApi,
    Custom(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CaptureMode {
    SystemAudio,
}

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Audio capture error: {0}")]
    AudioCaptureError(String),
    #[error("Audio processing error: {0}")]
    AudioProcessingError(String),
    #[error("VAD error: {0}")]
    VadError(String),
    #[error("STT error: {0}")]
    SttError(String),
    #[error("Streaming error: {0}")]
    StreamingError(String),
    #[error("Configuration error: {0}")]
    ConfigError(String),
    #[error("Internal error: {0}")]
    Internal(String),
}
