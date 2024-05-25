import socket
import sys
import time
from random import choice
from random import randint
from string import ascii_uppercase
from datetime import datetime
from datetime import timedelta
import uuid


level = ['alert','default','info','abobas']


class Event:
    def __init__(self):
        self.time = datetime.now() + timedelta(days=randint(1,365),minutes=randint(0,59),seconds=randint(0,59))
        self.level = choice(level)
        self.pid = randint(1,9999)
        self.event_id = choice(ascii_uppercase) + str(randint(1,1000))
        self.id = uuid.uuid4()

    def __str__(self):
        return f'{self.id} {self.time} {self.level} {self.pid} {self.event_id}'


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
            time.sleep(DELAY_MILLIS / 1000)
            ev = Event()
            print(ev)
            conn.sendall(str(ev).encode('ascii'))