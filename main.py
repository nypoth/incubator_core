#!/usr/bin/python

#  Official datasheet available from :
#  https://www.bosch-sensortec.com/bst/products/all_products/bme280

# import time
# from datetime import datetime
#
# import src.db.utility as db_uti
# from src.SPI.BME280 import Bme280
# from src.db.models.atmospheric import Atmospheric
# import src.custom_logging as clg
# import paho.mqtt.client as mqtt

#
# clg.setup_logger()
# lg = clg.get_logger(__name__)
#
# # definizione indirizzo del sensore
# sens = Bme280(1023)
#
# client = mqtt.Client()
#
# client.connect("localhost", 1883, 60)
#
# count = 0
# while True:
#
#     temperature, humidity, pressure = sens.bme280.temperature, sens.bme280.humidity, sens.bme280.pressure
#     lg.info(f'Timestamp: {datetime.now().astimezone()}')
#     lg.info(f'Temperatura: {temperature}°C')
#     lg.info(f'Umidità: {humidity}%')
#     lg.info(f'Pressione: {pressure}hPa')
#
#     client.publish("temperature", round(temperature, 2))
#     client.publish("humidity", round(humidity, 2))
#     client.publish("pressure", round(pressure, 2))
#
#     count += 1
#     if count > 30:
#         count = 0
#         lg.info('Salvataggio dati')
#         # Inserimento nuovo record su DB
#         db_uti.insert_data(
#                 Atmospheric,
#                 timestamp=datetime.now().astimezone(),
#                 temperature=temperature,
#                 humidity=humidity,
#                 pressure=pressure
#         )
#     time.sleep(1)
import logging
import os
try:
    import src.loadEnv
except:
    raise Exception("Impossibile importare la configurazione")

from src.Incubator import Incubator
from src.db.models.data import ConfigSchema
from src.db.utils import is_query_exception


from src.SPI.BME280 import Bme280
from src.db.ctrls.data import get_settings
from src.mqtt.core import MqttConnector

# Inizializzazione logger
logging.basicConfig(level=logging.DEBUG)
lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)

# Connessione broker MQTT
mq = MqttConnector(os.environ.get('CLIENT_ID'), os.environ.get('MQTT_BROKER_ADDRESS'), int(os.environ.get('MQTT_BROKER_PORT')))

# definizione indirizzo del sensore
sens = Bme280(1023)

res = get_settings()


lg.info(res)
if is_query_exception(res):
    raise Exception('Errore recupero impostazioni')

settings = ConfigSchema().dump(res)['value']

incubator = Incubator(mq, sens.bme280, settings)

while True:
    incubator()
