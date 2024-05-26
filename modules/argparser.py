import argparse
from collector import InetDevice

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