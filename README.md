


# 🔐 Secure MQTT with TLS Mutual Authentication

A demonstration of **end-to-end MQTT security** using **TLS mutual authentication** between a Python-based **publisher** and **subscriber**, with **Mosquitto** as the secure broker.

🌡️ The publisher simulates temperature readings.  
📺 The subscriber renders a live **terminal dashboard** using the `rich` library.

---

## 🗂️ Project Structure

```
Secure-MQTT/
├── certs/                   # 🔐 SSL/TLS certificates & keys
│   ├── ca.crt               # Certificate Authority (CA)
│   ├── ca.key
│   ├── client.crt
│   ├── client.key
│   ├── client.csr
│   ├── server.crt
│   ├── server.key
│   ├── server.csr
│   ├── openssl.cnf
│   └── ca.srl
├── mosquitto-secure.conf    # 🧾 Mosquitto TLS configuration
├── publisher.py             # 📤 Simulated temperature publisher
├── subscriber.py            # 📥 Real-time dashboard (rich)
├── .gitignore
└── README.md
```

---

## ⚙️ Mosquitto TLS Configuration

```conf
listener 8883
cafile certs/ca.crt
certfile certs/server.crt
keyfile certs/server.key

require_certificate true
use_identity_as_username true
allow_anonymous false
log_type all
```

✅ **What this config does:**

- 🔒 Enables TLS encryption
- 📛 Enforces client certificate verification
- 🧾 Uses Common Name (CN) as identity
- 🚫 Disables anonymous access

---

## 🔐 Certificate Generation (OpenSSL)

### 🔸 Step 1: Create a Certificate Authority (CA)
```bash
openssl genrsa -out certs/ca.key 2048
openssl req -x509 -new -nodes -key certs/ca.key -sha256 -days 365 -out certs/ca.crt -subj "/CN=MQTT-CA"
```

### 🔸 Step 2: Generate Server Certificate
```bash
openssl genrsa -out certs/server.key 2048
openssl req -new -key certs/server.key -out certs/server.csr -subj "/CN=localhost"
openssl x509 -req -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/server.crt -days 365 -sha256
```

### 🔸 Step 3: Generate Client Certificate
```bash
openssl genrsa -out certs/client.key 2048
openssl req -new -key certs/client.key -out certs/client.csr -subj "/CN=client"
openssl x509 -req -in certs/client.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/client.crt -days 365 -sha256
```

---

## 🐍 `publisher.py` – Simulated Temperature Publisher

Simulates temperature values and securely publishes to the broker.

```python
import paho.mqtt.client as mqtt
import time, random

def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code", rc)

client = mqtt.Client()
client.on_connect = on_connect

client.tls_set("certs/ca.crt", certfile="certs/client.crt", keyfile="certs/client.key")
client.tls_insecure_set(True)
client.connect("localhost", 8883)
client.loop_start()

try:
    while True:
        temperature = round(random.uniform(20.0, 30.0), 2)
        message = f"Temperature: {temperature}°C"
        client.publish("iot/test", message)
        print("Published:", message)
        time.sleep(3)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
```

---

## 🖥 `subscriber.py` – Terminal Dashboard (`rich`)

Displays real-time messages from the broker in a styled terminal table.

```python
from rich.console import Console
from rich.table import Table
import paho.mqtt.client as mqtt
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

console = Console()
table = Table(title="📡 Secure MQTT Dashboard")
table.add_column("Topic", style="cyan")
table.add_column("Payload", style="green")

def on_connect(client, userdata, flags, rc):
    console.print(f"[bold green]Connected to broker with code {rc}[/]")
    client.subscribe("iot/test")

def on_message(client, userdata, msg):
    table.add_row(msg.topic, msg.payload.decode())
    console.clear()
    console.print(table)

client = mqtt.Client()
client.tls_set("certs/ca.crt", certfile="certs/client.crt", keyfile="certs/client.key")
client.tls_insecure_set(False)
client.on_connect = on_connect
client.on_message = on_message

console.print("[bold blue]Starting Terminal Dashboard...[/]")
client.connect("localhost", 8883)

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    console.print("[bold red]Disconnected from broker.[/]")
```

---

## ▶️ How to Run

> Make sure Python & Mosquitto are installed.

1. 🧠 **Start the secure broker**
```bash
mosquitto -c mosquitto-secure.conf
```

2. 📥 **Start the subscriber dashboard**
```bash
python3 subscriber.py
```

3. 📤 **Launch the publisher**
```bash
python3 publisher.py
```

---

## 📌 Notes & Tips

- 🔐 Broker listens on **port 8883**
- ⚠️ Mutual TLS = client and server **both require certificates**
- 🎨 `rich` makes terminal output pretty:
  ```bash
  pip install rich
  ```

---

## 👨‍🏫 Author

Project created as part of a class presentation on  
**"Sécurité des communications et chiffrement dans l’IoT"**  
by **Abahazem**


