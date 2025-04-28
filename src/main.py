"""
Main service: read sensor, infer, publish, and alert.
"""
import time
from sensor_reader import SensorReader
from mqtt_client import MqttClient
from edge_model import EdgeModel
from alert_manager import AlertManager
import boto3
import os

# Config from env or defaults
ENDPOINT = os.getenv('IOT_ENDPOINT')
ROOT_CA = os.getenv('ROOT_CA_PATH')
CERT = os.getenv('CERT_PATH')
KEY = os.getenv('PRIVATE_KEY_PATH')
CLIENT_ID = 'temp-monitor-pi'
TOPIC = 'sensors/temperature'

if __name__ == '__main__':
    reader = SensorReader()
    mqtt = MqttClient(CLIENT_ID, ENDPOINT, 8883, ROOT_CA, KEY, CERT)
    mqtt.connect()
    sns = boto3.client('sns')
    model = EdgeModel(threshold=float(os.getenv('THRESHOLD', 70)))
    alert_mgr = AlertManager(mqtt_client=mqtt, sns_client=sns)

    history = []
    while True:
        temp = reader.read_temperature()
        ts = int(time.time())
        mqtt.publish(TOPIC, {'timestamp': ts, 'temp_c': temp})

        history.append(temp)
        if len(history) > 10:
            history.pop(0)
        if model.predict_overheat(temp):
            msg = alert_mgr.generate_message(history)
            alert_mgr.send_alert(msg)

        time.sleep(5)