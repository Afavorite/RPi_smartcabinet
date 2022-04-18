import requests
from PyQt5.QtCore import QThread, pyqtSignal

import temp_get


class ThreadHttp(QThread):
    SignalHttp = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        url = "http://39.107.226.190:8080/smartcabinet_server/rpiservlet"
        temp_get.setup()
        while True:
            temperature = temp_get.read()
            payload = {'temp': str(round(temperature, 2)), 'signal': 'without_lock', 'lock': 'unlock', 'ster': 'off'}
            r = requests.post(url, params=payload)
            # r_list = r.json()
            # self.SignalHttp.emit(r_list)
            print(r.content)
