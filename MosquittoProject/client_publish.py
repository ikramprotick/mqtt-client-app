#!/usr/bin/env python3
import ssl
import time
import logging
import paho.mqtt.client as mqtt

RULE_HOST = "136.186.230.175"     
USERNAME  = "protick"
PASSWORD  = "protick"
CA_PATH   = "ca.crt"
TOPIC     = f"{USERNAME}/data"
PUBLISH_INTERVAL = 5  


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[Publisher] %(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)

class MQTTPublisher:
    def __init__(self, host, username, password, ca_path, topic):
        self.host = host
        self.username = username
        self.password = password
        self.ca_path = ca_path
        self.topic = topic

        # Create the client and assign callbacks
        self.client = mqtt.Client(client_id="publisher_alt")
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

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
        else:
            logging.error(f"Failed to connect, result code {rc}")

    def on_publish(self, client, userdata, mid):
        logging.debug(f"Message {mid} published.")

    def connect_and_loop(self):
        """Connect to broker and start the loop in a background thread."""
        self.client.connect(self.host, port=8883, keepalive=60)
        self.client.loop_start()

    def publish_loop(self, interval_s):
        """Publish a numbered payload to self.topic every interval_s seconds."""
        counter = 0
        try:
            while True:
                payload = f"Payload #{counter}"
                result = self.client.publish(self.topic, payload=payload, qos=0)
                status = result.rc
                if status == mqtt.MQTT_ERR_SUCCESS:
                    logging.info(f"Published to {self.topic}: {payload}")
                else:
                    logging.error(f"Failed to publish message, rc={status}")
                counter += 1
                time.sleep(interval_s)
        except KeyboardInterrupt:
            logging.info("Interrupted by user, stopping publisher.")
        finally:
            self.cleanup()

    def cleanup(self):
        """Stop the loop and disconnect cleanly."""
        self.client.loop_stop()
        self.client.disconnect()
        logging.info("Disconnected from broker.")


if __name__ == "__main__":
    publisher = MQTTPublisher(
        host=RULE_HOST,
        username=USERNAME,
        password=PASSWORD,
        ca_path=CA_PATH,
        topic=TOPIC
    )
    publisher.connect_and_loop()
    publisher.publish_loop(interval_s=PUBLISH_INTERVAL)
