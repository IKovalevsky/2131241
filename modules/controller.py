from collector import Collector
from aggregator import Aggregator, Filter
from correlator import Correlator, EventRequest, EventResponse
from argparser import *


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
            try:
                cmd = self.__parser.parse_args(input('>>>').split())
                self.__actions[cmd.command](cmd)
            except SystemExit:
                pass


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
