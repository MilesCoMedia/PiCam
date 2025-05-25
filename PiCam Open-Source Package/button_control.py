import time
import subprocess
import os
import signal
from gpiozero import Button
import sys

# Configuration
BUTTON_PIN = 24
REBOOT_HOLD = 3  # seconds
DELETE_HOLD = 10  # seconds
PRESS_TIMEOUT = 2  # seconds between presses

# Global state
press_count = 0
last_press_time = 0
press_start_time = 0
running = True

# Set up button
button = Button(BUTTON_PIN)

def button_pressed():
    global press_start_time
    press_start_time = time.time()

def button_released():
    global press_count, last_press_time
    duration = time.time() - press_start_time
    current_time = time.time()
    
    # Check hold actions first
    if duration >= DELETE_HOLD:
        delete_video_files()
        return
    elif duration >= REBOOT_HOLD:
        reboot_pi()
        return
    
    # Handle press count
    if current_time - last_press_time < PRESS_TIMEOUT:
        press_count += 1
    else:
        press_count = 1
    
    last_press_time = current_time
    
    print(f"Button pressed {press_count} times")
    
    if press_count == 3:
        toggle_hotspot()
        press_count = 0
    elif press_count >= 5:
        shutdown_script()

def toggle_hotspot():
    print("Toggling hotspot...")
    try:
        result = subprocess.run(
            ["sudo", "toggle-hotspot"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hotspot error: {e.stderr}")

def delete_video_files():
    print("Deleting video files...")
    try:
        subprocess.run(
            ["sudo", "rm", "-rf", "/home/picam/videos/*"],
            check=True
        )
        print("All video files deleted")
    except subprocess.CalledProcessError as e:
        print(f"Delete error: {str(e)}")

def reboot_pi():
    print("Rebooting system...")
    try:
        subprocess.run(["sudo", "reboot"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Reboot failed: {str(e)}")

def shutdown_script():
    global running
    print("Shutting down all processes...")
    try:
        # Kill child processes
        subprocess.run(["pkill", "-P", str(os.getpid())], check=True)
        # Kill this script
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception as e:
        print(f"Shutdown error: {str(e)}")
    finally:
        running = False
        sys.exit(0)

# Configure button events
button.when_pressed = button_pressed
button.when_released = button_released

print("Button control system ready:")
print("- Triple click: Toggle hotspot")
print("- 5 clicks: Full shutdown")
print("- Hold 3s: Reboot")
print("- Hold 10s: Delete files")

try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    shutdown_script()
