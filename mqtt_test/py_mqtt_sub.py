import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "172.20.10.2"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_TOPIC = "embedded/test"

# rc: the connection result
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode('utf-8')}")
    #print(f"{msg.topic} - data1: {json.loads(msg.payload)['data1']}, data2: {json.loads(msg.payload)['data2']}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
# 設置登錄賬號和密碼
mqtt_client.username_pw_set("chris", "123456")
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)
mqtt_client.loop_forever()