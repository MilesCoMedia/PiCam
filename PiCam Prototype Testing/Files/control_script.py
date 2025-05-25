#!/usr/bin/env python3
import os
import signal

COMMAND_PIPE = "/tmp/camera_commands"
PID_FILE = "/tmp/recording_script.pid"

def send_stop_command():
    try:
        # Send stop command
        with open(COMMAND_PIPE, 'w') as pipe:
            pipe.write("stop\n")
        
        # Send signal to trigger immediate processing
        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGUSR1)
            print("UNE005 Stop command sent successfully")
        else:
            print("UNE002 Error: No running instance found")
    except Exception as e:
        print(f"UNE003 Error sending command: {str(e)}")

if __name__ == "__main__":
    send_stop_command()
