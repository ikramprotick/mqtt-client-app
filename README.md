# 🔌 MQTT Client App (Mosquitto + Python)

This repository contains a simple **MQTT client application in Python** with separate scripts for **publishing** and **subscribing** to MQTT topics.  
It’s designed for testing or learning MQTT with a broker such as **Mosquitto**.

---

## 📁 Project Structure

```text
mqtt-client-app/
└── MosquittoProject/
    ├── client_publish.py      # Publishes messages to an MQTT topic
    ├── client_subscribe.py    # Subscribes to an MQTT topic and prints messages
    ├── ca.crt                 # CA certificate for SSL/TLS (if enabled)
    └── README.md              # (Optional) Project documentation
