use anyhow::Result;
use shared_types::{AudioChunk, TranscriptionResult};

pub trait SttEngine: Send + Sync {
    fn transcribe(&mut self, audio: &[f32], sample_rate: u32) -> Result<TranscriptionResult>;
    fn transcribe_chunk(&mut self, chunk: &AudioChunk) -> Result<TranscriptionResult> {
        self.transcribe(&chunk.data, chunk.sample_rate)
    }
}
