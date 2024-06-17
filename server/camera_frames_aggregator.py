"""Aggregates camera streams and serves a React app to view them."""

# TODO: Consider using socketserver.UDPServer instead.
import socket

class CameraFramesAggregator:

    DEFAULT_ROUTER_IP = '192.168.1.1'
    DEFAULT_NETWORK_BROADCAST_IP = '192.168.1.255'
    DEFAULT_SERVER_IP = '192.168.1.156'
    LOCALHOST = '127.0.0.1'
    PORT_HTTP = 80
    PORT_HTTPS = 443
    PORT_LISTEN_DEFAULT = 42069

    def __init__(self) -> None:
        self.__ip_address = self._get_ip_address()

        # AF_INET is the address family for IPv4. SOCK_DGRAM is the socket type for UDP.
        # self.__socket_broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.__socket_broadcaster.sendto(b'Hello, world!', (CameraFramesAggregator.DEFAULT_NETWORK_BROADCAST_IP, CameraFramesAggregator.PORT_LISTEN_DEFAULT))

        self.__socket_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket_receiver.bind((self.__ip_address, CameraFramesAggregator.PORT_LISTEN_DEFAULT))
        # Since this socket is for UDP, it is connectionless and therefore does not need to listen().
        # See https://stackoverflow.com/questions/8194323/why-the-listen-function-call-is-not-needed-when-use-udp-socket.
        # See https://superuser.com/questions/1096504/why-udp-does-not-show-listening-in-the-state-column-in-netstat

        # print(self.__socket_receiver.getsockname())

    def run(self) -> None:
        # TODO: Broadcast this device's IP address to 192.168.1.255 so that clients can discover it
        # TODO: Spawn a new thread to listen on the socket for camera frames from the clients
        try:
            while True:
                pass
        finally:
            self._cleanup()

    @property
    def device_ip(self):
        return self.__ip_address

    def _get_ip_address(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect this socket to the router's IP address (though any IP would work for our purpose here).
            # This causes the socket to be bound, but we're not going to use it after this.
            s.connect((CameraFramesAggregator.DEFAULT_ROUTER_IP, CameraFramesAggregator.PORT_HTTP))
        except Exception as e:
            return 'Unable to determine IP address'
        else:
            return s.getsockname()[0]
        finally:
            s.close()

    def _cleanup(self) -> None:
        # self.__socket_broadcaster.close()
        self.__socket_receiver.close()

if __name__ == '__main__':
    server = CameraFramesAggregator()
    print(f'Server IP address: {server.device_ip}')

    server.run()