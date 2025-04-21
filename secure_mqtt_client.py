import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 8883
TOPIC = "iot/test"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)
    client.publish(TOPIC, "Hello, MQTT over TLS!")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

client = mqtt.Client()
client.username_pw_set("abahazem", "abahazem")

client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs="certs/ca.crt")
client.tls_insecure_set(True)  # ⬅️ This skips hostname validation
client.connect(BROKER, PORT)
client.loop_forever()
