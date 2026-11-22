use shared_types::{AudioChunk, VadEvent};

pub struct VadConfig {
    pub energy_threshold: f32,
    pub speech_min_duration_ms: u32,
    pub silence_min_duration_ms: u32,
}

impl Default for VadConfig {
    fn default() -> Self {
        Self {
            energy_threshold: 0.015,
            speech_min_duration_ms: 250,
            silence_min_duration_ms: 600,
        }
    }
}

pub trait VoiceActivityDetector: Send + Sync {
    fn process_chunk(&mut self, chunk: &AudioChunk) -> VadEvent;
    fn reset(&mut self);
}

pub struct EnergyVad {
    config: VadConfig,
}

impl EnergyVad {
    pub fn new(config: VadConfig) -> Self {
        Self { config }
    }

    pub fn calculate_rms(samples: &[f32]) -> f32 {
        if samples.is_empty() {
            return 0.0;
        }
        let sum_sq: f32 = samples.iter().map(|&s| s * s).sum();
        (sum_sq / samples.len() as f32).sqrt()
    }
}

impl VoiceActivityDetector for EnergyVad {
    fn process_chunk(&mut self, chunk: &AudioChunk) -> VadEvent {
        let rms = Self::calculate_rms(&chunk.data);
        let is_speech = rms >= self.config.energy_threshold;
        let confidence = (rms / (self.config.energy_threshold * 2.0)).min(1.0);

        VadEvent {
            is_speech,
            timestamp_ms: chunk.timestamp_ms,
            confidence,
        }
    }

    fn reset(&mut self) {}
}

pub struct SpeechSegmenter {
    vad: Box<dyn VoiceActivityDetector>,
    config: VadConfig,
    accumulated_samples: Vec<f32>,
    in_speech: bool,
    speech_start_ms: u64,
    silence_start_ms: u64,
}

impl SpeechSegmenter {
    pub fn new(config: VadConfig) -> Self {
        let vad = Box::new(EnergyVad::new(VadConfig {
            energy_threshold: config.energy_threshold,
            speech_min_duration_ms: config.speech_min_duration_ms,
            silence_min_duration_ms: config.silence_min_duration_ms,
        }));
        Self {
            vad,
            config,
            accumulated_samples: Vec::new(),
            in_speech: false,
            speech_start_ms: 0,
            silence_start_ms: 0,
        }
    }

    pub fn process(&mut self, chunk: &AudioChunk) -> Option<AudioChunk> {
        let event = self.vad.process_chunk(chunk);

        if event.is_speech {
            if !self.in_speech {
                self.in_speech = true;
                self.speech_start_ms = chunk.timestamp_ms;
                self.accumulated_samples.clear();
            }
            self.silence_start_ms = 0;
            self.accumulated_samples.extend_from_slice(&chunk.data);
            None
        } else if self.in_speech {
            self.accumulated_samples.extend_from_slice(&chunk.data);
            if self.silence_start_ms == 0 {
                self.silence_start_ms = chunk.timestamp_ms;
            } else if chunk.timestamp_ms.saturating_sub(self.silence_start_ms)
                >= self.config.silence_min_duration_ms as u64
            {
                // Silence duration reached -> emit completed speech segment
                self.in_speech = false;
                let duration = chunk.timestamp_ms.saturating_sub(self.speech_start_ms);
                if duration >= self.config.speech_min_duration_ms as u64 {
                    let segment = AudioChunk {
                        data: std::mem::take(&mut self.accumulated_samples),
                        timestamp_ms: self.speech_start_ms,
                        sample_rate: chunk.sample_rate,
                    };
                    return Some(segment);
                } else {
                    self.accumulated_samples.clear();
                }
            }
            None
        } else {
            None
        }
    }
}
