import os
import time
import datetime
import subprocess
import logging
import signal
from picamera2 import Picamera2
import psutil

# Configuration
COMMAND_PIPE = "/tmp/camera_commands"
PID_FILE = "/tmp/recording_script.pid"
VIDEO_DIR = "/home/picam/videos"

# Error Codes Dictionary
ERROR_CODES = {
    "CFG001": "Settings file not found",
    "CFG002": "Invalid setting value in config",
    "CFG003": "Missing required setting in config",
    "WIFI001": "Wi-Fi scan failed",
    "VID001": "Failed to start recording",
    "VID002": "Failed to stop recording",
    "VID003": "Video conversion failed",
    "DEL001": "File deletion failed",
    "DIR001": "Directory creation failed",
    "CAM001": "Camera initialization failed"
}

# Configure logging
logging.basicConfig(
    filename='/home/picam/recording.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CameraController:
    def __init__(self):
        self.picam2 = None
        self.recording = False
        self.current_file = None
        self.start_time = None
        self.running = True
        self.setup_signal_handlers()
        self.initialize_camera()
        self.setup_command_pipe()

    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGUSR1, self.signal_handler)

    def setup_command_pipe(self):
        if not os.path.exists(COMMAND_PIPE):
            os.mkfifo(COMMAND_PIPE)
            
    def check_commands(self):
        try:
            if os.path.exists(COMMAND_PIPE):
                with open(COMMAND_PIPE, 'r') as pipe:
                    command = pipe.read().strip()
                    if command == "stop":
                        logging.info("SHU002 Received stop command")
                        self.graceful_shutdown()
        except Exception as e:
            logging.error(f"UNE001Error reading command pipe: {str(e)}")

    def graceful_shutdown(self):
        self.stop_recording()
        self.close_camera()
        self.cleanup_resources()
        logging.info("SHU001 Script stopped gracefully")
        exit(0)

    def signal_handler(self, signum, frame):
        if signum in [signal.SIGINT, signal.SIGTERM]:
            self.graceful_shutdown()
        elif signum == signal.SIGUSR1:
            self.check_commands()

    def initialize_camera(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                kill_camera_processes()
                self.picam2 = Picamera2()
                config = self.picam2.create_video_configuration(
                    main={"size": (1920, 1080)},
                    controls={"FrameRate": 25}
                )
                self.picam2.configure(config)
                self.picam2.start()
                logging.info("Camera initialized successfully")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"CAM001: Camera initialization failed: {str(e)}")
                    raise
                logging.warning(f"Camera init failed (attempt {attempt+1}), retrying...")
                time.sleep(2)
                kill_camera_processes()

    def close_camera(self):
        if self.picam2 is not None:
            try:
                self.picam2.stop()
                self.picam2.close()
                logging.info("Camera resources released")
            except Exception as e:
                logging.error(f"Error closing camera: {str(e)}")
            finally:
                self.picam2 = None

    def cleanup_resources(self):
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        if os.path.exists(COMMAND_PIPE):
            os.remove(COMMAND_PIPE)

    def start_recording(self):
        if not self.recording and self.picam2 is not None:
            try:
                timestamp = datetime.datetime.now().strftime("Recording_%d-%m-%y_%H-%M-%S")
                self.current_file = f"{VIDEO_DIR}/{timestamp}.h264"
                self.picam2.start_recording(self.current_file)
                self.recording = True
                self.start_time = time.time()
                logging.info(f"Started recording: {self.current_file}")
            except Exception as e:
                logging.error(f"VID001: Failed to start recording: {str(e)}")
                self.recording = False

    def stop_recording(self):
        if self.recording and self.picam2 is not None:
            try:
                self.picam2.stop_recording()
                self.recording = False
                self.convert_to_mp4()
                self.current_file = None
                self.start_time = None
                logging.info("Stopped recording")
            except Exception as e:
                logging.error(f"VID002: Failed to stop recording: {str(e)}")

    def convert_to_mp4(self):
        if self.current_file and os.path.exists(self.current_file):
            try:
                mp4_path = self.current_file.replace('.h264', '.mp4')
                cmd = ["ffmpeg", "-y", "-i", self.current_file, "-c", "copy", mp4_path]
                subprocess.run(cmd, check=True)
                os.remove(self.current_file)
                logging.info(f"Converted {self.current_file} to MP4")
            except Exception as e:
                logging.error(f"VID003: Conversion failed: {str(e)}")

def kill_camera_processes():
    try:
        for proc in psutil.process_iter():
            try:
                if "libcamera" in proc.name():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        time.sleep(1)
    except Exception as e:
        logging.error(f"Error killing camera processes: {str(e)}")

def load_settings():
    settings = {
        "record_length": 10,
        "delete_after_days": 7,
        "wifi_ssid": "FoxtelHub3677"
    }
    try:
        with open("/home/picam/config.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().lower().replace(' ', '_')
                    value = value.strip()
                    if key == "record_length":
                        settings[key] = int(value)
                    elif key == "delete_after_days":
                        settings[key] = int(value)
                    elif key == "wifi_ssid":
                        settings[key] = value
        logging.info("Config loaded successfully")
    except FileNotFoundError:
        logging.error("CFG001: Config file not found, using defaults")
    except ValueError as e:
        logging.error(f"CFG002: Invalid value in config: {str(e)}")
    except Exception as e:
        logging.error(f"CFG003: Config error: {str(e)}")
    return settings

def delete_old_videos(days, video_dir):
    now = time.time()
    cutoff = now - (days * 86400)
    try:
        for filename in os.listdir(video_dir):
            if filename.startswith("Recording_") and filename.endswith(".mp4"):
                file_path = os.path.join(video_dir, filename)
                try:
                    file_time = os.path.getmtime(file_path)
                    if file_time < cutoff:
                        os.remove(file_path)
                        logging.info(f"Deleted old file: {filename}")
                except Exception as e:
                    logging.error(f"DEL001: Failed to delete {filename}: {str(e)}")
    except Exception as e:
        logging.error(f"DEL001: Directory scan failed: {str(e)}")

def main():
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    settings = load_settings()
    
    try:
        os.makedirs(VIDEO_DIR, exist_ok=True)
    except Exception as e:
        logging.error(f"DIR001: Could not create directory: {str(e)}")
        return

    camera = CameraController()
    last_scan = time.time()
    last_cleanup = time.time()

    try:
        while camera.running:
            current_time = time.time()
            
            # Check for external commands
            camera.check_commands()

            # Check Wi-Fi status
            if current_time - last_scan > 30:
                try:
                    result = subprocess.run(
                        ["iwlist", "wlan0", "scan"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        timeout=15
                    )
                    wifi_available = settings["wifi_ssid"] in result.stdout
                    
                    if wifi_available and camera.recording:
                        logging.info("Wi-Fi available, stopping recording")
                        camera.stop_recording()
                    elif not wifi_available and not camera.recording:
                        logging.info("Wi-Fi unavailable, starting recording")
                        camera.start_recording()
                    
                    last_scan = current_time
                except Exception as e:
                    logging.error(f"WIFI001: Scan failed: {str(e)}")

            # Check recording duration
            if camera.recording and (current_time - camera.start_time) > (settings["record_length"] * 60):
                logging.info("Maximum duration reached, rotating recording")
                camera.stop_recording()
                camera.start_recording()

            # Cleanup old files
            if current_time - last_cleanup > 3600:
                try:
                    delete_old_videos(settings["delete_after_days"], VIDEO_DIR)
                    last_cleanup = current_time
                except Exception as e:
                    logging.error(f"DEL001: Cleanup failed: {str(e)}")

            time.sleep(1)

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
    finally:
        camera.cleanup_resources()
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

if __name__ == "__main__":
    main()
