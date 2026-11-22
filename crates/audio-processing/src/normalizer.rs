pub struct AudioNormalizer {
    target_peak: f32,
}

impl AudioNormalizer {
    pub fn new() -> Self {
        Self { target_peak: 0.95 }
    }

    pub fn normalize(&self, samples: &[f32]) -> Vec<f32> {
        if samples.is_empty() {
            return Vec::new();
        }

        // Calculate DC offset (mean)
        let sum: f32 = samples.iter().sum();
        let dc_offset = sum / samples.len() as f32;

        // Remove DC offset and find maximum absolute peak
        let mut max_abs: f32 = 0.0;
        let centered: Vec<f32> = samples
            .iter()
            .map(|&s| {
                let v = s - dc_offset;
                let abs = v.abs();
                if abs > max_abs {
                    max_abs = abs;
                }
                v
            })
            .collect();

        // Scale to target peak if non-zero
        if max_abs > 0.0001 {
            let gain = (self.target_peak / max_abs).min(10.0); // max 20dB gain boost
            centered.into_iter().map(|s| (s * gain).clamp(-1.0, 1.0)).collect()
        } else {
            centered
        }
    }
}
