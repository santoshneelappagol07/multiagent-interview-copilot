use thiserror::Error;

#[derive(Error, Debug)]
pub enum DesktopError {
    #[error("Audio error: {0}")]
    Audio(String),
    #[error("Sidecar error: {0}")]
    Sidecar(String),
    #[error("Internal error: {0}")]
    Internal(String),
}

impl From<DesktopError> for String {
    fn from(err: DesktopError) -> Self {
        err.to_string()
    }
}
