import paho.mqtt.client as mqtt
import json
import time

# MQTT Settings
broker_address = "192.168.1.149"  # Update to your Raspberry Pi's IP address
port = 1883
username = "BB1"  # MQTT Username
password = "XXX"  # MQTT Password
subscribe_topics = ["esp32/status/+", "esp32/sensors/+"]

# MQTT Client Setup
# Specify the MQTT version 5.0 on client initialization
client = mqtt.Client("PiBrain", protocol=mqtt.MQTTv5)

# Set the username and password for MQTT broker
client.username_pw_set(username, password)

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code "+str(rc))
    # Subscribe to all topics of interest
    for topic in subscribe_topics:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    topic = msg.topic
    data = json.loads(msg.payload.decode())
    print(f"Data received from {topic}: {data}")
    # Decision-making based on data
    process_data(topic, data)

def process_data(topic, data):
    # Example processing function
    if "sensors" in topic:
        if data['distance'] < 30:  # Too close to an object
            take_action('stop')
        elif data['distance'] > 100:  # Safe distance
            take_action('moveForward')
    elif "status" in topic:
        if data['battery'] < 20:  # Low battery
            take_action('returnHome')

def take_action(command):
    # Publish command to ESP32
    client.publish("esp32/commands", command)
    print(f"Action taken: {command}")

try:
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address, port=port)
    client.loop_start()  # Start the loop in a non-blocking way
    while True:
        time.sleep(1)  # Keep the main thread alive
except Exception as e:
    print(f"Failed to connect or start MQTT loop: {e}")
