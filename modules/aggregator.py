import multiprocessing as mp
import sqlite3


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


class aggregator:
    def __init__(self, queqe) -> None:
        self.queqe = queqe

    def parsing(self):
        #парсинг
        pass

    def filter(self):
        #фильтрует как-то 
        pass

    def bd(self):
        #запись в бд 
        pass

        