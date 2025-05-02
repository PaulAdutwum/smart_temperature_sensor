"""
alert_manager.py
Generates human‑friendly overheat alerts with OpenAI and dispatches them via MQTT and/or SNS.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import List, Optional

import openai
from openai.error import OpenAIError
from paho.mqtt.client import Client as MqttClient
import boto3
from botocore.exceptions import BotoCoreError, ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

openai.api_key = OPENAI_API_KEY


class AlertManager:
    def __init__(
        self,
        mqtt_client: Optional[MqttClient] = None,
        sns_client: Optional[boto3.client] = None,
    ) -> None:
        self.mqtt = mqtt_client
        self.sns = sns_client or boto3.client("sns")

    # ---------- OpenAI ----------
    @staticmethod
    def _generate_message(temps: List[float]) -> str:
        """Return a concise, friendly overheat alert based on recent temperatures."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an IoT assistant generating short alerts.",
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Temperature history in °C: {temps}. "
                            "Write a brief alert for non‑technical users."
                        ),
                    },
                ],
                max_tokens=60,
            )
            return response.choices[0].message["content"].strip()
        except OpenAIError as exc:
            logging.error("OpenAI request failed: %s", exc)
            raise

    # ---------- Publish ----------
    def send_alert(self, temps: List[float]) -> None:
        """Generate a message and publish via MQTT and/or SNS."""
        message = self._generate_message(temps)
        payload = json.dumps({"alert": message, "timestamp": time.time()})

        if self.mqtt:
            logging.info("Publishing alert to MQTT")
            self.mqtt.publish("alerts/overheat", payload, qos=1, retain=False)

        if SNS_TOPIC_ARN:
            try:
                logging.info("Publishing alert to SNS")
                self.sns.publish(Message=payload, TopicArn=SNS_TOPIC_ARN)
            except (BotoCoreError, ClientError) as exc:
                logging.error("SNS publish failed: %s", exc)


# ------------------------- CLI demo -------------------------
if __name__ == "__main__":
    # Example usage: simulate an alert with dummy data
    example_temps = [24.5, 25.1, 26.3, 29.0, 31.2]  # °C
    manager = AlertManager(mqtt_client=None)  # supply an MQTT client in production
    manager.send_alert(example_temps)
