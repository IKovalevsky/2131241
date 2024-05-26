import argparse
from datetime import datetime
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
        parser.add_argument('-n', '--name', help='username', required=False, type=str)

    @staticmethod
    def add_all(subparsers):
        DeviceAction.__add(subparsers)
        DeviceAction.__remove(subparsers)
        DeviceAction.__show(subparsers)


class FilterAction:
    add = 'add-filter'
    remove = 'remove-filter'
    show = 'show-filter'

    @staticmethod
    def __add(subparsers):
        parser = subparsers.add_parser(FilterAction.add, help='211221')
        parser.add_argument('-d', '--device_name', help='foo help', required=True)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-td', '--time_duration', help='seconds', required=False, type=int)
        group.add_argument('-tt', '--time_to', help='seconds', required=False, type=int)
        parser.add_argument('-n', '--name', help='filter name', required=False, type=str)

    @staticmethod
    def __remove(subparsers):
        parser = subparsers.add_parser(FilterAction.remove, help='dfsfsdfsd')
        parser.add_argument('-n', '--name', help='username', required=True, type=str)

    @staticmethod
    def __show(subparsers):
        parser = subparsers.add_parser(FilterAction.show, help='dfsfsdfsd')
        parser.add_argument('-n', '--name', help='username', required=False, type=str)

    @staticmethod
    def add_all(subparsers):
        FilterAction.__add(subparsers)
        FilterAction.__remove(subparsers)
        FilterAction.__show(subparsers)


class CorrelatorAction:
    get = 'get-event'

    @staticmethod
    def __get(subparsers):
        parser = subparsers.add_parser(CorrelatorAction.get, help='211221')
        parser.add_argument('-l', '--level', help='foo help', required=False)
        parser.add_argument('-td', '--time_duration', help='seconds', required=False, type=int)
        parser.add_argument('-tt', '--time_to', help='seconds', required=False, type=int)
        parser.add_argument('-tf', '--time_from', help='seconds', required=False, type=int)

    @staticmethod
    def add_all(subparsers):
        CorrelatorAction.__get(subparsers)


class ProgramAction:
    exit = 'exit'

    @staticmethod
    def add_all(subparsers):
        parser = subparsers.add_parser(ProgramAction.exit, help='211221')


class Parser:

    def __init__(self):
        self.__parser = argparse.ArgumentParser('SIEM')
        subparsers = self.__parser.add_subparsers(dest='command', help='sdsdsds')
        DeviceAction.add_all(subparsers)
        FilterAction.add_all(subparsers)
        CorrelatorAction.add_all(subparsers)
        ProgramAction.add_all(subparsers)
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
            self.__switches.remove(name)
        if name in self.__windows:
            self.__windows.remove(name)
        print(f'Removing device {name}')

    def show(self, name: str) -> None:
        print('SW: ' + ' '.join(self.__switches))
        print('Win: ' + ' '.join(self.__windows))


class Filter:

    def __init__(self, device_name, name, time_duration, time_to):
        self.device_name = device_name
        self.name = name
        self.time_duration = time_duration
        self.time_to = time_to


class Aggregator:

    def __init__(self):
        self.__filters = set()

    def add(self, filter_rule: Filter) -> None:
        self.__filters.add(filter_rule.name)
        print(f'Adding filter {filter_rule.name}')

    def remove(self, name: str):
        if name in self.__filters:
            self.__filters.remove(name)
        print(f'Removing filter {name}')

    def show(self, name: str) -> None:
        print('Filters: ' + ' '.join(self.__filters))


class EventRequest:
    def __init__(self, level, time_from, time_to, duration):
        pass


class EventResponse:
    def __init__(self):
        self.time = datetime.now()
        self.level = 'HIGH'
        self.device_name = 'SW1'

    def __str__(self):
        return f'{self.time} {self.level} {self.device_name}'


class Correlator:

    def get(self, request: EventRequest) -> list[EventResponse]:
        return [EventResponse(), EventResponse()]


class Controller:
    def __init__(self):

        self.__collector = Collector()
        self.__aggregator = Aggregator()
        self.__correlator = Correlator()

        self.__parser = Parser()
        self.__actions = {DeviceAction.add: self.__device_do_add,
                          DeviceAction.remove: self.__device_do_remove,
                          DeviceAction.show: self.__device_do_show,
                          FilterAction.add: self.__filter_do_add,
                          FilterAction.remove: self.__filter_do_remove,
                          FilterAction.show: self.__filter_do_show,
                          CorrelatorAction.get: self.__correlator_do_get,
                          ProgramAction.exit: lambda cmd: exit(0)}

    def run(self):
        while True:
            cmd = self.__parser.parse_args(input('>>>').split())
            self.__actions[cmd.command](cmd)

    def __correlator_do_get(self, cmd):
        request = EventRequest(cmd.level, cmd.time_duration, cmd.time_to, cmd.time_from)
        print('\n'.join(str(r) for r in self.__correlator.get(request)))

    def __filter_do_add(self, cmd):
        filter_rule = Filter(cmd.device_name, cmd.name, cmd.time_duration, cmd.time_to)
        self.__aggregator.add(filter_rule)

    def __filter_do_remove(self, cmd):
        self.__aggregator.remove(cmd.name)

    def __filter_do_show(self, cmd):
        self.__aggregator.show(cmd.name)

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
