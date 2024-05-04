import paho.mqtt.client as mqtt
import json
import time

# MQTT Settings
broker_address = "192.168.1.149"  # Your Raspberry Pi's IP address
port = 1883
username = "BB1"  # MQTT Username
password = "XXX"  # MQTT Password
subscribe_topics = ["esp32/status/+", "esp32/sensors/+"]

# Create an MQTT client instance
# Ensure compatibility by not specifying the protocol version explicitly here
client = mqtt.Client("PiBrain")

# Set MQTT username and password
client.username_pw_set(username, password)

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in subscribe_topics:
        client.subscribe(topic)

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode('utf-8'))
    print(f"Received message '{payload}' on topic '{topic}' with QoS {msg.qos}")
    process_data(topic, payload)

def process_data(topic, data):
    if "sensors" in topic:
        if data['distance'] < 30:  # Too close
            take_action('stop')
        elif data['distance'] > 100:  # Safe distance
            take_action('move_forward')
    elif "status" in topic:
        if data['battery'] < 20:  # Low battery
            take_action('return_home')

def take_action(command):
    # Send a command to the ESP32
    client.publish("esp32/commands", json.dumps({"command": command}))
    print(f"Sent command: {command}")

try:
    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(broker_address, port=port)
    client.loop_forever()  # Start the loop
except Exception as e:
    print(f"Error connecting or during MQTT loop: {e}")
