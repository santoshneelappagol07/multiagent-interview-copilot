pub mod proto {
    tonic::include_proto!("audio_service");
}

use anyhow::Result;
use proto::audio_service_server::{AudioService, AudioServiceServer};
use proto::*;
use std::net::SocketAddr;
use std::pin::Pin;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use tokio::sync::broadcast;
use tokio_stream::{wrappers::BroadcastStream, Stream, StreamExt};
use tonic::{Request, Response, Status};
use tracing::info;

pub struct AudioServiceImpl {
    is_running: Arc<AtomicBool>,
    tx: broadcast::Sender<TranscriptionEvent>,
}

impl AudioServiceImpl {
    pub fn new(tx: broadcast::Sender<TranscriptionEvent>) -> Self {
        Self {
            is_running: Arc::new(AtomicBool::new(false)),
            tx,
        }
    }
}

#[tonic::async_trait]
impl AudioService for AudioServiceImpl {
    type StreamTranscriptionsStream =
        Pin<Box<dyn Stream<Item = Result<TranscriptionEvent, Status>> + Send + 'static>>;

    async fn stream_transcriptions(
        &self,
        _request: Request<EmptyRequest>,
    ) -> Result<Response<Self::StreamTranscriptionsStream>, Status> {
        let rx = self.tx.subscribe();
        let stream = BroadcastStream::new(rx).filter_map(|res| res.ok()).map(Ok);
        Ok(Response::new(Box::pin(stream)))
    }

    async fn get_status(
        &self,
        _request: Request<EmptyRequest>,
    ) -> Result<Response<EngineStatusResponse>, Status> {
        Ok(Response::new(EngineStatusResponse {
            is_running: self.is_running.load(Ordering::SeqCst),
            device_name: "Default System Audio Output (Loopback)".to_string(),
            sample_rate: 16000,
            uptime_ms: 1000,
        }))
    }

    async fn start_capture(
        &self,
        _request: Request<StartCaptureRequest>,
    ) -> Result<Response<StartCaptureResponse>, Status> {
        self.is_running.store(true, Ordering::SeqCst);
        Ok(Response::new(StartCaptureResponse {
            success: true,
            message: "System audio capture started".to_string(),
        }))
    }

    async fn stop_capture(
        &self,
        _request: Request<EmptyRequest>,
    ) -> Result<Response<StopCaptureResponse>, Status> {
        self.is_running.store(false, Ordering::SeqCst);
        Ok(Response::new(StopCaptureResponse { success: true }))
    }

    async fn list_devices(
        &self,
        _request: Request<EmptyRequest>,
    ) -> Result<Response<DeviceListResponse>, Status> {
        Ok(Response::new(DeviceListResponse {
            devices: vec![AudioDevice {
                id: "default".to_string(),
                name: "System Audio Loopback (Default Output)".to_string(),
                is_default: true,
            }],
        }))
    }
}

pub async fn start_grpc_server(
    addr: SocketAddr,
    tx: broadcast::Sender<TranscriptionEvent>,
) -> Result<()> {
    let service = AudioServiceImpl::new(tx);
    info!("Starting audio gRPC streaming server on {}", addr);
    tonic::transport::Server::builder()
        .add_service(AudioServiceServer::new(service))
        .serve(addr)
        .await?;
    Ok(())
}
