import multiprocessing as mp
import socket
from re import match
from enum import Enum, unique


class InetDevice:
    @unique
    class Type(Enum):
        switch = 'switch'
        windows = 'windows'

        def __str__(self):
            return self.value

    def __init__(self, ip_address: str, port: int, name: str):
        if not self.__validate_ip(ip_address):
            raise ValueError("Invalid IP Address")
        if not self.__validate_port(port):
            raise ValueError("Invalid Port")

        self.ip_address = ip_address
        self.port = port
        self.name = name

    def __str__(self):
        return f'{self.ip_address}:{self.port} {self.name}'

    @staticmethod
    def __validate_ip(address: str):
        return match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', address)

    @staticmethod
    def __validate_port(port: int):
        return port > 1000


class Collector:

    def __init__(self):
        self.__switches = set()
        self.__windows = set()

    def add_switch(self, device: InetDevice) -> None:
        self.__switches.add(device.name)
        print(f'Adding switch {device.name}')

    def add_windows(self, device: InetDevice) -> None:
        self.__windows.add(device.name)
        print(f'Adding windows {device.name}')

    def remove(self, name: str):
        if name in self.__switches:
            self.__switches.remove(name)
        if name in self.__windows:
            self.__windows.remove(name)
        print(f'Removing device {name}')

    def show(self, name: str) -> None:
        print('SW: ' + ' '.join(self.__switches))
        print('Win: ' + ' '.join(self.__windows))


class collector:
    def __init__(self, queue):
        self.queue = queue

    def listen_tcp_service(self, host, port):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            print(f"[+] Connecting to {host}:{port}...")

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                log_string = data.decode('utf-8').strip()
                # print(log_string)
                self.queue.put(log_string)

        except (ConnectionRefusedError, ConnectionResetError, socket.error) as e:
            print(e)

        finally:
            while True:
                if not queue.empty():
                    print(queue.get(block=False))
            client_socket.close()
            print(f"[!] {host}:{port} - connection dropped.")

    def start(self, host, ports):
        processes = []
        for port in ports:
            process = mp.Process(target=self.listen_tcp_service, args=(host, port))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()


if __name__ == '__main__':
    queue = mp.Queue()
    listener = collector(queue)
    listener.start('127.0.0.1', [10000, 10001])
