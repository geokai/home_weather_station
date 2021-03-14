#!/usr//bin/env python3

# Author: George Kaimakis
# Source:   https://github.com/geokai/home_weather_station
# This file was created on 12/27/19


from datetime import datetime
import socket
import select
import time
from to_str import to_str


def recvd_time():
    """generate a timestamp - uses 'time_ns' as a work-around to
    eliminate the nonseconds (a hack)
    """
    ts = int(time.time_ns()/1000000000)
    recv_time = datetime.fromtimestamp(ts)
    return recv_time


def console_output(temp, baro, hum, tUnit):
    """process the parameters and return a formatted string"""
    return '\rTemperature: {0:.1f} {3}\tBarometer: {1:.1f} hPa/mB\tHumidity: {2:.1f} %RH' \
            .format(temp, baro, hum, tUnit)


class SocketServer:
    """Simple socket server that listens to one single client."""

    def __init__(self, host='0.0.0.0', port=42042):
        """Initialize the server with a host and port to listen to."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)

    def close_server(self):
        """Close the server socket."""
        print(" :Closing server socket (host {}, port {})\n".format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None

    def run_server(self):
        """Accept and handle an incoming connection."""
        print("Starting server socket (host {}, port {})".format(self.host, self.port))
        print()

        while True:
            client_sock, client_addr = self.sock.accept()

            # print("Client {} connected at: {}".format(client_addr, recvd_time()))

            stop = False
            while not stop:
                if client_sock:
                    # Check if the client is still connected and if data is available:
                    try:
                        rdy_read, rdy_write, sock_err = select.select([client_sock, ], [], [])
                        # print()
                        # print(rdy_read)
                        # print()
                    except select.error:
                        print("Select() failed on socket with {}.".format(client_addr))
                        return 1

                    if len(rdy_read) > 0:
                        read_data = client_sock.recv(255)
                        # Check if socket has been closed by client:
                        if len(read_data) == 0:
                            # print("{} closed the socket.".format(client_addr))
                            stop = True
                            break  # keep the server socket open (in outer loop)
                        else:
                            msg = to_str(read_data)   # convert bytes to str
                            # print(">>> Received:\n{}\n".format(msg.rstrip()))
                            print("{},{}".format(recvd_time(), msg.rstrip()))
                            # client_sock.send(b'recv: '+read_data)   # ack
                else:
                    print("No client connected.")
                    # print("No client is connected, waiting for a client to connect.")
                    # print("No client is connected, SocketServer can't receive data")
                    stop = True
                    return
            # Close socket:
            # print("Closing connection with {}.".format(client_addr))
            # print()
            # print()
            # print("No client is connected, waiting for a client to connect...")
            # print()
            # print()
            client_sock.close()


def main():
    """Start socket server."""
    server = SocketServer()
    try:
        server.run_server()
    except KeyboardInterrupt:
        server.close_server()
    finally:
        quit()


if __name__ == "__main__":
    main()
