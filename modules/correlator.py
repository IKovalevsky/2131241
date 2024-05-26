from datetime import datetime


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