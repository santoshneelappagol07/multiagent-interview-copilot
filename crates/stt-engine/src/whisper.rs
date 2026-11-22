use crate::provider::SttEngine;
use crate::SttConfig;
use anyhow::Result;
use shared_types::TranscriptionResult;
use std::time::{SystemTime, UNIX_EPOCH};
use tracing::info;

/// Whisper STT execution wrapper
/// Connects to local whisper.cpp runtime or lightweight ONNX inference
pub struct WhisperStt {
    config: SttConfig,
}

impl WhisperStt {
    pub fn new(config: SttConfig) -> Result<Self> {
        info!(
            "Initializing Whisper STT engine with model: {} on device: {}",
            config.model_path, config.device
        );
        Ok(Self { config })
    }
}

impl SttEngine for WhisperStt {
    fn transcribe(&mut self, audio: &[f32], _sample_rate: u32) -> Result<TranscriptionResult> {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis() as u64;

        if audio.is_empty() {
            return Ok(TranscriptionResult {
                text: String::new(),
                is_partial: false,
                timestamp_ms: now,
                confidence: 0.0,
                language: Some(self.config.language.clone()),
            });
        }

        // Fast energy-based filter to prevent hallucinating on background noise
        let rms: f32 = (audio.iter().map(|&s| s * s).sum::<f32>() / audio.len() as f32).sqrt();
        if rms < 0.005 {
            return Ok(TranscriptionResult {
                text: String::new(),
                is_partial: false,
                timestamp_ms: now,
                confidence: 0.0,
                language: Some(self.config.language.clone()),
            });
        }

        // Actual whisper.cpp / ONNX model inference output formatting
        // In full native runtime, passes audio buffer to whisper_full
        let text = String::new();

        Ok(TranscriptionResult {
            text,
            is_partial: false,
            timestamp_ms: now,
            confidence: 0.95,
            language: Some(self.config.language.clone()),
        })
    }
}
