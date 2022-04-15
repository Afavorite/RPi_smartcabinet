import time
from threading import Thread

import requests

import temp_get


class ThreadHttp(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        url = "http://39.107.226.190:8080/smartcabinet_server/rpiservlet"
        temp_get.setup()
        while True:
            temperature = temp_get.read()
            payload = {'1010_temp': str(round(temperature, 2))}
            r = requests.post(url, params=payload)
            time.sleep(1)

            print(r.content)