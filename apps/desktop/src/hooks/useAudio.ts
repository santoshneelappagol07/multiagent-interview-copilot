import { invoke } from '@tauri-apps/api/core';
import { useAppStore } from '../stores/appStore';

export function useAudio() {
  const isCapturing = useAppStore((state) => state.isCapturing);
  const setCapturing = useAppStore((state) => state.setCapturing);

  const startCapture = async () => {
    try {
      await invoke('start_audio_capture');
      setCapturing(true);
    } catch (err) {
      console.error('Failed to start audio loopback capture:', err);
    }
  };

  const stopCapture = async () => {
    try {
      await invoke('stop_audio_capture');
      setCapturing(false);
    } catch (err) {
      console.error('Failed to stop audio loopback capture:', err);
    }
  };

  const toggleCapture = () => {
    if (isCapturing) {
      stopCapture();
    } else {
      startCapture();
    }
  };

  return { isCapturing, startCapture, stopCapture, toggleCapture };
}
