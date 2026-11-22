use crate::error::DesktopError;
use std::path::PathBuf;
use std::sync::Arc;
use tokio::process::{Child, Command};
use tokio::sync::Mutex;
use tracing::{error, info};

pub struct SidecarManager {
    process: Arc<Mutex<Option<Child>>>,
}

impl SidecarManager {
    pub fn new(process: Arc<Mutex<Option<Child>>>) -> Self {
        Self { process }
    }

    pub async fn start_backend(&self, root_dir: PathBuf) -> Result<(), DesktopError> {
        let mut guard = self.process.lock().await;
        if guard.is_some() {
            info!("Python backend process is already running");
            return Ok(());
        }

        let backend_dir = root_dir.join("apps").join("backend");
        #[cfg(target_os = "windows")]
        let python_exe = backend_dir.join(".venv").join("Scripts").join("python.exe");
        #[cfg(not(target_os = "windows"))]
        let python_exe = backend_dir.join(".venv").join("bin").join("python");

        let child = Command::new(&python_exe)
            .args(["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"])
            .current_dir(&backend_dir)
            .spawn()
            .map_err(|e| DesktopError::Sidecar(format!("Failed to start Python backend: {}", e)))?;

        *guard = Some(child);
        info!("Python FastAPI backend sidecar started");
        Ok(())
    }

    pub async fn stop_backend(&self) -> Result<(), DesktopError> {
        let mut guard = self.process.lock().await;
        if let Some(mut child) = guard.take() {
            if let Err(e) = child.kill().await {
                error!("Error terminating Python backend sidecar: {}", e);
            }
            info!("Python FastAPI backend sidecar stopped");
        }
        Ok(())
    }
}
