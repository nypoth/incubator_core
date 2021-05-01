from src.db.ctrls.data import insert_data
from src.db.models.data import Atmospheric
from schedule import every, repeat, run_pending

from src.mqtt.core import MqttConnector


class Incubator:

    def __init__(self, mqtt: MqttConnector, sensors, config):
        self.mqtt = mqtt
        self.sensors = sensors
        self.config = config

    def __call__(self, *args, **kwargs):
        run_pending()

    @repeat(every(10).minutes)
    def acquire_sensor_data(self):

        temperature, humidity, pressure = self.sensors.temperature, self.sensors.humidity, self.sensors.pressure

        self._save_sensor_data(temperature, humidity, pressure)

    @staticmethod
    def _save_sensor_data(temperature, humidity, pressure):
        data = Atmospheric()
        data.temperature = temperature
        data.humidity = humidity
        data.temperature = pressure

        insert_data(data)

    def send_data(self):
        self.mqtt._client.publish('')
