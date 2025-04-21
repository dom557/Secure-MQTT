import paho.mqtt.client as mqtt
import time
import random  # to simulate temperature

def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code", rc)

client = mqtt.Client()
client.username_pw_set("abahazem", "abahazem")
client.on_connect = on_connect

client.tls_set(ca_certs="certs/ca.crt")
client.tls_insecure_set(True)
client.connect("localhost", 8883)

client.loop_start()  # use loop_start to allow sending messages in background

try:
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)  # simulate temperature between 20.0°C and 30.0°C
        message = f"Temperature: {temperature}°C"
        client.publish("iot/test", message)
        print("Published:", message)
        time.sleep(3) #kola 3 second kayrsl temp .
except KeyboardInterrupt:
    print("Stopped by user.")
    client.loop_stop()
    client.disconnect()
