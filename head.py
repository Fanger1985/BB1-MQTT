import paho.mqtt.client as mqtt
import json
import time

broker_address = "192.168.1.149"  # Updated IP address
port = 1883
username = "BB1"  # MQTT Username
password = "XXX"  # MQTT Password

client = mqtt.Client("PiBrain")
client.username_pw_set(username, password)  # Set username and password

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to topics here
    client.subscribe("esp32/status/+")
    client.subscribe("esp32/sensors/+")

def on_message(client, userdata, msg):
    # Your message handling
    print(f"Message received on {msg.topic}: {msg.payload.decode()}")

# Setup connection
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker_address, port=port)
    client.loop_forever()
except Exception as e:
    print(f"Failed to connect or start MQTT loop: {e}")
