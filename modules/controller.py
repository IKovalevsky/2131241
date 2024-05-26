import argparse
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


class DeviceAction:
    add = 'add-device'
    remove = 'remove-device'
    show = 'show-device'

    @staticmethod
    def __add(subparsers):
        parser = subparsers.add_parser(DeviceAction.add, help='211221')
        parser.add_argument('-t', '--type', help='foo help', required=True, type=InetDevice.Type,
                            choices=list(InetDevice.Type))
        parser.add_argument('-ip', '--ip_address', help='bar help', required=True, type=str)
        parser.add_argument('-p', '--port', help='bar help', required=True, type=int)
        parser.add_argument('-n', '--name', help='username', required=True, type=str)

    @staticmethod
    def __remove(subparsers):
        parser = subparsers.add_parser(DeviceAction.remove, help='dfsfsdfsd')
        parser.add_argument('-n', '--name', help='username', required=True, type=str)

    @staticmethod
    def __show(subparsers):
        parser = subparsers.add_parser(DeviceAction.show, help='dfsfsdfsd')
        parser.add_argument('-t', '--type', help='foo help', required=False, type=InetDevice.Type,
                            choices=list(InetDevice.Type))

    @staticmethod
    def add_all(subparsers):
        DeviceAction.__add(subparsers)
        DeviceAction.__remove(subparsers)
        DeviceAction.__show(subparsers)


class Parser:

    def __init__(self):
        self.__parser = argparse.ArgumentParser('SIEM')
        subparsers = self.__parser.add_subparsers(dest='command', help='sdsdsds')
        DeviceAction.add_all(subparsers)

        self.__parser.print_help()

    def parse_args(self, arg_list):
        return self.__parser.parse_args(arg_list)


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
            del self.__switches[name]
        if name in self.__windows:
            del self.__windows[name]
        print(f'Removing device {name}')

    def show(self) -> None:
        print('SW: ' + ' '.join(self.__switches))
        print('Win: ' + ' '.join(self.__windows))


class Controller:
    def __init__(self):

        self.__collector = Collector()

        self.__parser = Parser()
        self.__actions = {DeviceAction.add: self.__device_do_add,
                          DeviceAction.remove: self.__device_do_remove,
                          DeviceAction.show : self.__device_do_show}

    def run(self):
        while True:
            cmd = self.__parser.parse_args(input('>>>').split())
            self.__actions[cmd.command](cmd)

    def __device_do_add(self, cmd):
        device = InetDevice(ip_address=cmd.ip_address, port=cmd.port, name=cmd.name)
        if cmd.type == InetDevice.Type.switch:
            self.__collector.add_switch(device)
        if cmd.type == InetDevice.Type.windows:
            self.__collector.add_windows(device)

    def __device_do_remove(self, cmd):
        self.__collector.remove(cmd.name)

    def __device_do_show(self, cmd):
        self.__collector.show(cmd.type)


Controller().run()