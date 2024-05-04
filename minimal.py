import paho.mqtt.client as mqtt

# Test MQTT Client Creation
try:
    client = mqtt.Client("TestClient", protocol=mqtt.MQTTv311)
    print("MQTT Client created successfully")
except Exception as e:
    print(f"Error creating MQTT client: {e}")

# Test connecting to a non-existent server to see if we can reach this point without errors
try:
    client.connect("localhost", 1883)
    print("Connection attempt successful, check your MQTT server setup")
except Exception as e:
    print(f"Error attempting to connect: {e}")
