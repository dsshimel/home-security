"""Aggregates camera streams and serves a React app to view them."""

import socket

class CameraFramesAggregator:

    DEFAULT_ROUTER_IP = '192.168.1.1'
    PORT_HTTP = 80
    PORT_HTTPS = 443

    def __init__(self) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__ip_address = self._get_ip_address()

    def run(self) -> None:
        # TODO: Broadcast this device's IP address to 192.168.1.255 so that clients can discover it
        # TODO: Spawn a new thread to listen on the socket for camera frames from the clients
        self._cleanup()

    @property
    def device_ip(self):
        return self.__ip_address

    def _get_ip_address(self) -> str:
        try:
            # Connect to the router's IP address
            self.__socket.connect((CameraFramesAggregator.DEFAULT_ROUTER_IP, 80))
            ip_address = self.__socket.getsockname()[0]
        except Exception as e:
            ip_address = 'Unable to determine IP address'
        return ip_address

    def _cleanup(self) -> None:
        self.__socket.close()

if __name__ == '__main__':
    server = CameraFramesAggregator()
    print(f'Server IP address: {server.device_ip}')

    server.run()