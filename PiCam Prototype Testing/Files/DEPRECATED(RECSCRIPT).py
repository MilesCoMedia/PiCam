import os
import time
import datetime
from picamera2 import Picamera2
from libcamera import controls
import subprocess
import logging

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

class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'error_code'):
            record.error_code = 'N/A'
        return super().format(record)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('/home/picam/recording.log')
formatter = CustomFormatter('%(asctime)s - %(levelname)s - [%(error_code)s] %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def log_error(error_code, message):
    logger.error(message, extra={'error_code': error_code})
    print(f"ERROR {error_code}: {message} - {ERROR_CODES.get(error_code, 'Unknown error')}")

def load_settings():
    settings = {
        "record_length": 600,
        "delete_after_days": 7,
        "wifi_ssid": "YOUR_HOME_NETWORK"
    }
    
    try:
        with open("/home/picam/config.txt", "r") as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    key = key.lower().replace(' ', '_')
                    if key == "record_length":
                        settings[key] = int(value) * 60
                    elif key == "delete_after_days":
                        settings[key] = int(value)
                    elif key == "wifi_ssid":
                        settings[key] = value.strip()
    except FileNotFoundError:
        log_error("CFG001", "Config file not found, using defaults")
    except ValueError as e:
        log_error("CFG002", f"Invalid value in config: {str(e)}")
    except Exception as e:
        log_error("CFG003", f"Config error: {str(e)}")
    return settings

def is_wifi_connected(ssid):
    try:
        result = subprocess.run(
            ["iwlist", "wlan0", "scan"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        return ssid in result.stdout
    except subprocess.TimeoutExpired:
        log_error("WIFI001", "Wi-Fi scan timed out")
    except Exception as e:
        log_error("WIFI001", f"Wi-Fi scan failed: {str(e)}")
    return False

def convert_to_mp4(h264_path):
    try:
        mp4_path = h264_path.replace('.h264', '.mp4')
        cmd = f"ffmpeg -framerate 15 -i {h264_path} -c copy {mp4_path}"
        subprocess.run(cmd, shell=True, check=True)
        os.remove(h264_path)
        return mp4_path
    except Exception as e:
        log_error("VID003", f"Conversion failed: {str(e)}")
        return h264_path

def delete_old_videos(days, video_dir):
    now = time.time()
    cutoff = now - (days * 86400)
    try:
        for filename in os.listdir(video_dir):
            if filename.startswith("Recording_"):
                file_path = os.path.join(video_dir, filename)
                try:
                    file_time = os.path.getmtime(file_path)
                    if file_time < cutoff:
                        os.remove(file_path)
                        logger.info(f"Deleted old file: {filename}")
                except Exception as e:
                    log_error("DEL001", f"Failed to delete {filename}: {str(e)}")
    except Exception as e:
        log_error("DEL001", f"Directory scan failed: {str(e)}")

def main():
    settings = load_settings()
    video_dir = "/home/picam/videos"
    
    try:
        os.makedirs(video_dir, exist_ok=True)
    except Exception as e:
        log_error("DIR001", f"Could not create directory: {str(e)}")
        return

    try:
        # Correct camera configuration for OV5647
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration(
            main={"size": (1920, 1080)},
            encode={"format": "h264"},  # Correct encoder specification
            controls={"FrameRate": 15}  # Reduced for OV5647 compatibility
        )
        picam2.configure(video_config)
        picam2.start()
        logger.info("Camera initialized successfully")
    except Exception as e:
        log_error("CAM001", f"Camera initialization failed: {str(e)}")
        return

    recording = False
    current_file = None
    start_time = None
    last_check = time.time()

    try:
        while True:
            if time.time() - last_check > 3600:
                delete_old_videos(settings["delete_after_days"], video_dir)
                last_check = time.time()

            wifi_available = is_wifi_connected(settings["wifi_ssid"])
            
            if not wifi_available:
                if not recording:
                    try:
                        timestamp = datetime.datetime.now().strftime("Recording_%d-%m-%y_%H-%M-%S")
                        current_file = os.path.join(video_dir, f"{timestamp}.h264")
                        picam2.start_recording(current_file)
                        recording = True
                        start_time = time.time()
                        logger.info(f"Started recording: {current_file}")
                    except Exception as e:
                        log_error("VID001", f"Recording start failed: {str(e)}")
                else:
                    elapsed = time.time() - start_time
                    if elapsed >= settings["record_length"]:
                        try:
                            picam2.stop_recording()
                            convert_to_mp4(current_file)
                            timestamp = datetime.datetime.now().strftime("Recording_%d-%m-%y_%H-%M-%S")
                            current_file = os.path.join(video_dir, f"{timestamp}.h264")
                            picam2.start_recording(current_file)
                            start_time = time.time()
                        except Exception as e:
                            log_error("VID001", f"Recording split failed: {str(e)}")
            else:
                if recording:
                    try:
                        picam2.stop_recording()
                        convert_to_mp4(current_file)
                        recording = False
                        current_file = None
                        start_time = None
                    except Exception as e:
                        log_error("VID002", f"Recording stop failed: {str(e)}")

            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Program stopped by user")
    finally:
        if recording:
            try:
                picam2.stop_recording()
                if current_file:
                    convert_to_mp4(current_file)
            except Exception as e:
                log_error("VID002", f"Final stop failed: {str(e)}")
        picam2.stop()
        picam2.close()

if __name__ == "__main__":
    main()
