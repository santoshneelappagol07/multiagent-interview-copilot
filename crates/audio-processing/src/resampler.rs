/// Linear interpolation resampler for low latency real-time conversion
pub struct LinearResampler {
    target_rate: u32,
}

impl LinearResampler {
    pub fn new(target_rate: u32) -> Self {
        Self { target_rate }
    }

    pub fn resample(&self, input: &[f32], source_rate: u32) -> Vec<f32> {
        if input.is_empty() || source_rate == self.target_rate {
            return input.to_vec();
        }

        let ratio = source_rate as f64 / self.target_rate as f64;
        let output_len = (input.len() as f64 / ratio).ceil() as usize;
        let mut output = Vec::with_capacity(output_len);

        for i in 0..output_len {
            let src_idx = i as f64 * ratio;
            let idx0 = src_idx.floor() as usize;
            let idx1 = (idx0 + 1).min(input.len() - 1);
            let frac = (src_idx - idx0 as f64) as f32;

            let sample = input[idx0] * (1.0 - frac) + input[idx1] * frac;
            output.push(sample);
        }

        output
    }
}
