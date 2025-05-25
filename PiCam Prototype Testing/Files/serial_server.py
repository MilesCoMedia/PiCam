import os
import socket
import threading
import subprocess
import time
import json
import logging
from gpiozero import Buzzer
from picamera2 import Picamera2
import psutil

# Configuration
SERIAL_FILE = "/home/pi/serialnumber.txt"
SERVER_IP = "192.168.4.1"
PORT = 4545
BUZZER_PIN = 11
HEALTH_CHECK_PATTERN = [0.2, 0.2, 0.5, 0.2, 0.2, 0.5]  # AirTag pattern
VIDEO_DIR = "/home/pi/videos"

# Configure logging
logging.basicConfig(
    filename='/home/pi/serial_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HealthChecker:
    def __init__(self):
        self.buzzer = Buzzer(BUZZER_PIN)
        self.camera = Picamera2()
        self.errors = []
        
    def _play_buzzer_pattern(self):
        try:
            for duration in HEALTH_CHECK_PATTERN:
                self.buzzer.on()
                time.sleep(duration)
                self.buzzer.off()
                time.sleep(0.1)
        except Exception as e:
            self.errors.append("BUZ001: Buzzer test failed")
            logging.error(f"Buzzer error: {str(e)}")
        finally:
            self.buzzer.close()

    def check_camera(self):
        try:
            config = self.camera.create_still_configuration()
            self.camera.configure(config)
            self.camera.start()
            self.camera.capture_file("/tmp/healthcheck.jpg")
            os.remove("/tmp/healthcheck.jpg")
            self.camera.stop()
        except Exception as e:
            self.errors.append("CAM002: Camera test failed")
            logging.error(f"Camera check failed: {str(e)}")
        finally:
            self.camera.close()

    def check_storage(self):
        try:
            stat = os.statvfs(VIDEO_DIR)
            available_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            if available_gb < 1:  # 1GB minimum
                self.errors.append("STR001: Low storage ({:.1f}GB)".format(available_gb))
        except Exception as e:
            self.errors.append("STR002: Storage check failed")
            logging.error(f"Storage error: {str(e)}")

    def check_system(self):
        try:
            # Check voltage
            throttled = subprocess.check_output(["vcgencmd", "get_throttled"]).decode().strip()
            if "0x50000" in throttled:
                self.errors.append("SYS001: Under-voltage detected")
                
            # Check temperature
            temp = float(subprocess.check_output(["vcgencmd", "measure_temp"])
                .decode().split("=")[1].split("'")[0])
            if temp > 85:
                self.errors.append("SYS002: High temperature ({:.1f}°C)".format(temp))
                
            # Check memory
            mem = psutil.virtual_memory()
            if mem.percent > 90:
                self.errors.append("SYS003: High memory usage ({:.1f}%)".format(mem.percent))
                
        except Exception as e:
            self.errors.append("SYS004: System check failed")
            logging.error(f"System check error: {str(e)}")

    def perform_full_check(self):
        self.check_camera()
        self._play_buzzer_pattern()
        self.check_storage()
        self.check_system()
        return self.errors

def get_serial_number():
    try:
        with open(SERIAL_FILE, "r") as f:
            return f.read().strip()
    except Exception as e:
        logging.error(f"Serial number error: {str(e)}")
        return "UNKNOWN"

def handle_client(conn):
    try:
        request = conn.recv(1024).decode().strip()
        logging.info(f"Received command: {request}")

        if request == "sendserialnumber":
            serial = get_serial_number()
            conn.send(serial.encode())
            
        elif request == "performHealthCheck":
            checker = HealthChecker()
            errors = checker.perform_full_check()
            response = json.dumps({
                "status": "OK" if not errors else "ERROR",
                "errors": errors
            })
            conn.send(response.encode())
            
        else:
            conn.send(b"Invalid command")
            
    except Exception as e:
        logging.error(f"Client handling error: {str(e)}")
    finally:
        conn.close()

def network_monitor():
    while True:
        try:
            # Check for preferred network availability
            scan = subprocess.check_output(["iwlist", "wlan0", "scan"], timeout=10)
            if b"Preferred_SSID" not in scan:  # Replace with your SSID
                logging.warning("Primary network unavailable")
        except Exception as e:
            logging.error(f"Network monitor error: {str(e)}")
        time.sleep(60)

def main():
    # Start network monitoring thread
    threading.Thread(target=network_monitor, daemon=True).start()
    
    # Set up TCP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((SERVER_IP, PORT))
        s.listen(5)
        logging.info(f"Server started on {SERVER_IP}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            logging.info(f"Connection from {addr}")
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
