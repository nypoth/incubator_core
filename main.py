import time

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

incubator = Incubator(mq, None)  # sens.bme280

while True:
    time.sleep(1)
