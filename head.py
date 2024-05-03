import paho.mqtt.client as mqtt
import json
import time

# MQTT Settings
broker_address = "192.168.1.100"  # Your Raspberry Pi IP
port = 1883
subscribe_topics = ["esp32/status/+", "esp32/sensors/+"]

# MQTT Client Setup
client = mqtt.Client("PiBrain")

def on_connect(client, userdata, flags, rc):
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

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=port)
client.loop_forever()
