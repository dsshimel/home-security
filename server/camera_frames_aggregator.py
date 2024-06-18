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
    UDP_BUFFER_SIZE = 65536

    def __init__(self) -> None:
        self.__ip_address = self._get_ip_address()
        # For simplicity, we'll skip broadcasting our IP and port to the network for now.

        # TODO: Given packet size constraints with UDP, consider using TCP/IP with SOCK_STREAM instead.
        # AF_INET is the address family for IPv4. SOCK_DGRAM is the socket type for UDP.
        # Since this socket is for UDP, it is connectionless and therefore does not need to listen().
        # See https://stackoverflow.com/questions/8194323/why-the-listen-function-call-is-not-needed-when-use-udp-socket.
        # See https://superuser.com/questions/1096504/why-udp-does-not-show-listening-in-the-state-column-in-netstat
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((self.__ip_address, CameraFramesAggregator.PORT_LISTEN_DEFAULT))

        # Set a timeout for the socket to prevent blocking indefinitely.
        # On Windows, Ctrl+C wasn't working until I added this.
        self.__socket.settimeout(1.0)

    def run(self) -> None:
        while True:
            try:
                data, address = self.__socket.recvfrom(CameraFramesAggregator.UDP_BUFFER_SIZE)
                print(f'Received {len(data)} bytes from {address}')
                print(f'Data: {data}')
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print('Server shutting down...')
                break

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
            return f'Unable to get IP address: {e}'
        else:
            return s.getsockname()[0]
        finally:
            s.close()

    def _cleanup(self) -> None:
        self.__socket.close()

if __name__ == '__main__':
    server = CameraFramesAggregator()
    print(f'Server IP address: {server.device_ip}')

    server.run()