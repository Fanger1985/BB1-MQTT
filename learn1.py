import requests
import time

# ESP32 Web Server configuration
ESP32_IP = '192.168.1.149'
PORT = 80

def send_command(command):
    """ Send HTTP GET request to ESP32 for specific movement commands. """
    url = f"http://{ESP32_IP}:{PORT}/{command}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully sent command '{command}'")
        else:
            print(f"Failed to send command '{command}', Status code: {response.status_code}")
    except Exception as e:
        print(f"Error with command '{command}': {e}")

def perform_figure_eight():
    """ Perform figure 8 by sequencing movements and turns. """
    # First leg
    send_command("forward")
    time.sleep(1)  # Adjust timing based on actual movement speed
    send_command("stop")
    time.sleep(0.5)

    # First curve
    send_command("left")
    time.sleep(0.5)  # Time for half turn
    send_command("stop")
    time.sleep(0.5)
    send_command("forward")
    time.sleep(1)
    send_command("stop")
    time.sleep(0.5)

    # Second curve
    send_command("right")
    time.sleep(1)  # Longer turn for reverse direction
    send_command("stop")
    time.sleep(0.5)
    send_command("forward")
    time.sleep(1)
    send_command("stop")
    time.sleep(0.5)

    # Final alignment
    send_command("left")
    time.sleep(0.5)  # Half turn to original direction
    send_command("stop")

def main():
    print("Starting Figure 8 Maneuver...")
    perform_figure_eight()
    print("Figure 8 Maneuver Complete.")

if __name__ == "__main__":
    main()
