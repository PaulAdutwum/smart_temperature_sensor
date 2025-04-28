"""
Reads temperature from DS18B20 via 1-Wire on Embedded Linux.
"""
from w1thermsensor import W1ThermSensor

class SensorReader:
    def __init__(self, sensor_id=None):
        self.sensor = W1ThermSensor(sensor_id)

    def read_temperature(self) -> float:
        """Return temperature in °C."""
        return self.sensor.get_temperature()