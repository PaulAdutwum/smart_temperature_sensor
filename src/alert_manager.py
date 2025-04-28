"""
Generates human-friendly alerts via OpenAI and sends via MQTT/SNS.
"""
import os
import openai

class AlertManager:
    def __init__(self, mqtt_client=None, sns_client=None):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.mqtt = mqtt_client
        self.sns = sns_client

    def generate_message(self, temps: list) -> str:
        prompt = (
            f"Temperature history (°C): {temps}. "
            "Create a concise alert about overheating."
        )
        resp = openai.Completion.create(
            engine='gpt-3.5-turbo',
            prompt=prompt,
            max_tokens=60
        )
        return resp.choices[0].text.strip()

    def send_alert(self, message: str):
        if self.mqtt:
            self.mqtt.publish('alerts', {'message': message})
        if self.sns:
            self.sns.publish(Message=message, TopicArn=os.getenv('SNS_TOPIC_ARN'))