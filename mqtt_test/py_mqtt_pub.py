import paho.mqtt.client as mqtt
import json
import random

MQTT_SERVER = "172.20.10.11" # 要連接的電腦的ip
MQTT_PORT = 1883 # port
MQTT_ALIVE = 60 # keepalive: the keepalive timeout value for the client. Defaults to 60 seconds.
MQTT_TOPIC = "embedded/test" # 訂閱的主題

mqtt_client = mqtt.Client()
# client_id :the MQTT client id to use. If “” or None, the Paho library will generate a client id automatically.
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)

def publish():
  payload = {
    'data1': random.random(),
    'data2': random.random()
  }
  print(f"payload: {payload}")
  mqtt_client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
  mqtt_client.loop(2,10)

no = 1

while no < 51:
  publish()
  no = no + 1