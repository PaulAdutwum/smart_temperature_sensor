"""
Read temperature from a DS18B20 sensor on Raspberry Pi.

Usage:
    python sensor_reader.py  # prints reading every second
"""
import os
import time
import logging
from typing import Optional

from w1thermsensor import W1ThermSensor, SensorNotReadyError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class SensorReader:
    def __init__(self, sensor_id: Optional[str] = None) -> None:
        """
        Parameters
        ----------
        sensor_id : str, optional
            ID of the DS18B20 probe. If None, use the first detected sensor.
        """
        self.sensor = W1ThermSensor(sensor_id)

    def read_temperature(self) -> float:
        """Return the current temperature in °C."""
        try:
            return self.sensor.get_temperature()
        except SensorNotReadyError as exc:
            logging.warning("Sensor not ready: %s", exc)
            raise


if __name__ == "__main__":
    reader = SensorReader(sensor_id=os.getenv("SENSOR_ID"))
    while True:
        try:
            temp = reader.read_temperature()
            logging.info("Temperature: %.2f °C", temp)
        except Exception as err:
            logging.error("Failed to read sensor: %s", err)
        time.sleep(1)
