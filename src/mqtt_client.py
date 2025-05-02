"""
aws_mqtt.py
Lightweight MQTT client for AWS IoT Core with mutual‑TLS auth.
"""
from __future__ import annotations

import json
import logging
import ssl
from pathlib import Path
from typing import Callable, Dict, Optional

import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class AwsMqttClient:
    """
    Parameters
    ----------
    client_id : str
    endpoint  : str   e.g. 'a3k7odshaiiotx-ats.iot.us-east-1.amazonaws.com'
    port      : int   usually 8883 for MQTT over TLS
    root_ca   : Path  AmazonRootCA1.pem
    cert_pem  : Path  <thing>-certificate.pem.crt
    priv_key  : Path  <thing>-private.pem.key
    """

    def __init__(
        self,
        client_id: str,
        endpoint: str,
        port: int,
        root_ca: Path,
        cert_pem: Path,
        priv_key: Path,
        on_message: Optional[Callable[[str, Dict], None]] = None,
    ) -> None:
        self._client = mqtt.Client(client_id=client_id, clean_session=True)
        self._client.tls_set(
            ca_certs=str(root_ca),
            certfile=str(cert_pem),
            keyfile=str(priv_key),
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )
        self._endpoint = endpoint
        self._port = port

        
        if on_message:
            def _wrapper(_cli, _userdata, msg):  # paho callback signature
                on_message(msg.topic, json.loads(msg.payload.decode()))
            self._client.on_message = _wrapper

    # ------------------------------------------------------------------
    def connect(self) -> None:
        logging.info("Connecting to AWS IoT Core at %s:%s", self._endpoint, self._port)
        self._client.connect(self._endpoint, self._port)
        self._client.loop_start()

    def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    # ------------------------------------------------------------------
    def publish(self, topic: str, payload: Dict, qos: int = 1, retain: bool = False) -> None:
        """Publish a JSON payload."""
        result = self._client.publish(topic, json.dumps(payload), qos=qos, retain=retain)
        result.wait_for_publish()
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            logging.error("Publish failed: rc=%s", result.rc)

    def subscribe(self, topic: str, qos: int = 1) -> None:
        """Subscribe to a topic; requires on_message callback to read."""
        self._client.subscribe(topic, qos=qos)
        logging.info("Subscribed to %s", topic)


# ------------- CLI Demo -------------
if __name__ == "__main__":
    from time import sleep
    import os

    ROOT_CA = Path("AmazonRootCA1.pem")
    CERT    = Path("device-cert.pem.crt")
    KEY     = Path("private.pem.key")
    ENDPOINT = os.getenv("AWS_IOT_ENDPOINT")  
    CLIENT_ID = "temp-sensor-demo"

    mqtt_cli = AwsMqttClient(
        client_id=CLIENT_ID,
        endpoint=ENDPOINT,
        port=8883,
        root_ca=ROOT_CA,
        cert_pem=CERT,
        priv_key=KEY,
    )

    mqtt_cli.connect()
    try:
        for i in range(5):
            mqtt_cli.publish("demo/hello", {"msg": f"hello #{i}"})
            sleep(1)
    finally:
        mqtt_cli.disconnect()
