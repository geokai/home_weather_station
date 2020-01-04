"""
Reads the temperature & humidity date from the am2320 sensor and sends
the date to the server via a socket
"""


# Author:   George Kaimakis
# Source:   https://github.com/geokai/home_weather_station
# Date:     03.12.2019


import socket
import time
import machine

import wifi

import am2320
import config


# create the i2c and sensor class objects:
i2c = machine.I2C(scl=machine.Pin(config.I2C_SCL), sda=machine.Pin(config.I2C_SDA))
sensor = am2320.AM2320(i2c=i2c)


def dots(*, num_of_dots=3, rate=0.5):
    """prints dots in a row (default 3) at a rate (default 0.5 secs)"""
    for i in range(num_of_dots):
        print('.', end='')
        time.sleep(rate)


def cel_or_fah():
    """determine the temperature unit from the config setting"""
    if config.FAHRENHEIT:
        tUnit = 'F'
    else:
        tUnit = 'C'
    return tUnit


def console_output(temp, hum, tUnit):
    """process the parameters and return a formatted string"""
    return '\rTemperature: {0:5.1f} {2}  \tHumidity: {1:5.1f} %RH' \
            .format(temp, hum, tUnit)


def read_sensor():
    """take a reading from the sensor and return the data"""
    # read the sensor:
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()

    if config.FAHRENHEIT:
        # celcius to fahrenheit conversion
        temperature = temperature * 9 / 5 + 32

    return temperature, humidity


def echo_client(msg):
    """attempt to connect to the socket server and send the msg (payload)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((config.HOST, config.PORT))
        s.sendall(msg)
        s.close()
    except Exception as e:
        pass


def main_loop():
    while True:
        temperature, humidity = read_sensor()
        tUnit = cel_or_fah()
        payload = '{0},{1:3.1f},{3},{2:3.1f}' \
                   .format(config.SENSOR_ID, temperature, humidity, tUnit)
        echo_client(payload)
        if config.DEBUG:
            dots()
            print("\r", console_output(temperature, humidity, tUnit))
        time.sleep(config.INTERVAL)


if __name__ == "__main__":
    wifi.connect_wifi()
    time.sleep(1)
    main_loop()
