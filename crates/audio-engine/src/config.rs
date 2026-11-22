use serde::{Deserialize, Serialize};
use shared_types::AudioConfig;
use stt_engine::SttConfig;
use vad_engine::VadConfig;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioEngineConfig {
    pub audio: AudioConfig,
    #[serde(skip)]
    pub vad: VadConfig,
    #[serde(skip)]
    pub stt: SttConfig,
    pub grpc_port: u16,
}

impl Default for AudioEngineConfig {
    fn default() -> Self {
        Self {
            audio: AudioConfig::default(),
            vad: VadConfig::default(),
            stt: SttConfig::default(),
            grpc_port: 50051,
        }
    }
}
