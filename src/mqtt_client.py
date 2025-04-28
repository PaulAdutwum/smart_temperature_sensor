"""
MQTT client for AWS IoT Core using TLS.
"""
import ssl
import json
import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, client_id, endpoint, port, root_ca, private_key, certificate):
        self.client = mqtt.Client(client_id)
        self.client.tls_set(
            ca_certs=root_ca,
            certfile=certificate,
            keyfile=private_key,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        self.endpoint = endpoint
        self.port = port

    def connect(self):
        self.client.connect(self.endpoint, self.port)
        self.client.loop_start()

    def publish(self, topic: str, payload: dict):
        self.client.publish(topic, json.dumps(payload))