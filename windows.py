import socket
import sys
import time
from random import choice
from random import choices
from random import randint
from string import ascii_uppercase
from datetime import datetime
from datetime import timedelta
import uuid

level = ['alert', 'default', 'info', 'abobas']
log_file = ''


class Event:
    def __init__(self):
        self.time = datetime.now() + timedelta(days=randint(1, 365), minutes=randint(0, 59), seconds=randint(0, 59))
        self.user = ''.join(choices(ascii_uppercase, k=randint(5, 15)))
        self.success = choice([True, False])
        self.level = choice(level)
        self.event_id = choice(ascii_uppercase) + str(randint(1, 1000))
        self.id = uuid.uuid4()

    def __str__(self):
        return f'{self.id} {self.time} {self.user} {self.success} {self.level} {self.event_id}'


def do_something(scheduler):
    global log_file
    global DELAY_MILLIS
    scheduler.enter(DELAY_MILLIS, 1, do_something, (scheduler,))


HOST = "127.0.0.1"
PORT = int(sys.argv[1])
DELAY_MILLIS = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            if len(log_file) > 1e4:
                log_file = ''
            log_file += str(Event()) + '\n'

            time.sleep(DELAY_MILLIS / 1000)
            conn.sendall(log_file.encode('ascii'))