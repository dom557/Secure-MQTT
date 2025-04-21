from rich.console import Console
from rich.table import Table
import paho.mqtt.client as mqtt
import warnings

#ignore the warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

console = Console()
table = Table(title="📡 Secure MQTT Dashboard")

table.add_column("Topic", style="cyan", no_wrap=True)
table.add_column("Payload", style="green")

BROKER = "localhost"
PORT = 8883
TOPIC = "iot/test"

def on_connect(client, userdata, flags, rc):
    console.print(f"[bold green]Connected to MQTT broker with code {rc}[/]")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    table.add_row(msg.topic, msg.payload.decode())
    console.clear()
    console.print(table)

client = mqtt.Client()  # ← connecting to MQTT client
client.username_pw_set("abahazem", "abahazem")
client.tls_set("certs/ca.crt")
client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message

console.print("[bold blue]Starting Terminal Dashboard...[/]")
client.connect(BROKER, PORT)
client.loop_forever()
