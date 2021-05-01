import math

import board
import busio
import digitalio
import adafruit_bme280


class Bme280:

    def __init__(self, sea_level_pressure=1023):
        spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
        cs = digitalio.DigitalInOut(board.D5)
        self.bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, cs)
        self.bme280.sea_level_pressure = sea_level_pressure

    def get_dew_point(self):
        b = 17.62
        c = 243.12
        gamma = (b * self.bme280.temperature / (c + self.bme280.temperature)) + math.log(self.bme280.humidity / 100.0)
        return (c * gamma) / (b - gamma)
