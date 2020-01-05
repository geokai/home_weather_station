"""
A robust wifi connection function
"""


import network
from time import sleep
import _inet_config


def connect_wifi():
    """deactivate the access point"""
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    """create the connection client and connect if not connected"""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to WiFi...')
        sta_if.active(True)
        sta_if.connect(_inet_config.WIFI_SSID, _inet_config.WIFI_PASSWORD)
        while not sta_if.isconnected():
            sleep(1)
    print('Network config: ', sta_if.ifconfig())


def disconnect_wifi():
    """Deactivate the network connection"""
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        print('Disconnecting from WiFi...')
        sta_if.active(False)
    print('Disconnected form WiFi.')
