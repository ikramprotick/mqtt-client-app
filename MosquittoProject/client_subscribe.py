#!/usr/bin/env python3
import ssl
import logging
import paho.mqtt.client as mqtt


RULE_HOST = "136.186.230.175"     
USERNAME  = "protick"
PASSWORD  = "protick"
CA_PATH   = "ca.crt"
PRIVATE_TOPIC = f"{USERNAME}/data"
PUBLIC_TOPIC  = "public/#"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[Subscriber] %(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)

class MQTTSubscriber:
    def __init__(self, host, username, password, ca_path, topics):
        self.host = host
        self.username = username
        self.password = password
        self.ca_path = ca_path
        self.topics = topics 

        self.client = mqtt.Client(client_id="subscriber_alt")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Configure credentials and TLS
        self.client.username_pw_set(self.username, self.password)
        self.client.tls_set(
            ca_certs=self.ca_path,
            certfile=None,
            keyfile=None,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )
        self.client.tls_insecure_set(True) 

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info(f"Connected to {self.host} with result code {rc}")
            # Subscribe to each topic
            for t in self.topics:
                client.subscribe(t)
                logging.info(f"Subscribed to: {t}")
        else:
            logging.error(f"Failed to connect, result code {rc}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode(errors="ignore")
        logging.info(f"Received on {msg.topic}: {payload}")

    def run(self):
        """Connect and block in loop_forever()."""
        self.client.connect(self.host, port=8883, keepalive=60)
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            logging.info("Interrupted by user, stopping subscriber.")
            self.client.disconnect()
            logging.info("Disconnected from broker.")


if __name__ == "__main__":
    subscriber = MQTTSubscriber(
        host=RULE_HOST,
        username=USERNAME,
        password=PASSWORD,
        ca_path=CA_PATH,
        topics=[PUBLIC_TOPIC, PRIVATE_TOPIC]
    )
    subscriber.run()
