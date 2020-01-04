"""Basic use of the am2320 temperature/humidity sensor"""


import time
import machine

import wifi
import am2320
import config


LOOP_INTERVAL = 28.5   # seconds


# create the i2c and sensor class objects:
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
sensor = am2320.AM2320(i2c=i2c)


def read_sens():
    """read data from sensor and return result (tuple)"""
    # read the sensor:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    if config.FAHRENHEIT:
        temperature = temperature * 9 / 5 + 32

    return temperature, humidity


def output_format(temp, hum):
    """process the parameters and return a formatted string"""
    if config.FAHRENHEIT:
        tUnit = 'F'
    else:
        tUnit = 'C'
    return '\rTemperature: {0:5.1f} {2}  \tHumidity: {1:5.1f} %RH' \
            .format(temp, hum, tUnit)


def dots(*, num_of_dots=3, rate=0.5):
    """prints dots in a row (default 3) at a rate (default 0.5 secs)"""
    for i in range(num_of_dots):
        print('.', end='')
        time.sleep(rate)


if __name__ == '__main__':
    wifi.connect_wifi()
    while True:
        dots()
        temperature, humidity = read_sens()
        print(output_format(temperature, humidity))
        time.sleep(LOOP_INTERVAL)
