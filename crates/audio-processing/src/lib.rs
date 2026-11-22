pub mod normalizer;
pub mod resampler;

use anyhow::Result;
use normalizer::AudioNormalizer;
use resampler::LinearResampler;
use shared_types::AudioChunk;

pub struct AudioProcessor {
    target_sample_rate: u32,
    normalizer: AudioNormalizer,
    resampler: LinearResampler,
}

impl AudioProcessor {
    pub fn new(target_sample_rate: u32) -> Self {
        Self {
            target_sample_rate,
            normalizer: AudioNormalizer::new(),
            resampler: LinearResampler::new(target_sample_rate),
        }
    }

    pub fn process(&mut self, chunk: AudioChunk) -> Result<AudioChunk> {
        // 1. Remove DC offset & peak normalize
        let normalized = self.normalizer.normalize(&chunk.data);

        // 2. Resample if input rate does not match target (e.g. 48kHz -> 16kHz for Whisper)
        let processed_data = if chunk.sample_rate != self.target_sample_rate {
            self.resampler.resample(&normalized, chunk.sample_rate)
        } else {
            normalized
        };

        Ok(AudioChunk {
            data: processed_data,
            timestamp_ms: chunk.timestamp_ms,
            sample_rate: self.target_sample_rate,
        })
    }
}
