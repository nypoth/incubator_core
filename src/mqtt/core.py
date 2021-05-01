import logging

import paho.mqtt.client as mqtt



class MqttConnector:

    def __init__(self, client_id, broker_address, broker_port):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('creazione istanza MqttConnector')
        # region mqtt
        self._client = mqtt.Client(client_id=client_id, clean_session=False, transport="tcp")
        # client.on_message = self.on_message
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.enable_logger(self.logger)
        self._client.connect(broker_address, broker_port, 120)
        self._client.loop_start()
        # endregion

    @property
    def connection(self):
        return self._client

    @property
    def state(self):
        return self._client.is_connected()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected with result code " + str(rc))

    def on_disconnect(self, client, userdata, rc):
        self.logger.error("1001 - Disconnessione dal broker")

    def on_message(self, client, userdata, msg):
        self.logger.info(msg.payload.decode())
