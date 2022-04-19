import requests
from PyQt5.QtCore import QThread, pyqtSignal

import temp_get


class ThreadHttp(QThread):
    SignalHttp = pyqtSignal(dict)
    lock = ''
    ster = ''

    def __init__(self):
        super().__init__()
        self.lock = 'lock'
        self.ster = 'off'

    def run(self):
        url = "http://39.107.226.190:8080/smartcabinet_server/rpiservlet"
        temp_get.setup()
        while True:
            temperature = temp_get.read()
            payload = {'temp': str(round(temperature, 2)), 'lock': self.lock, 'ster': self.ster}
            r = requests.post(url, params=payload)
            r_dict = r.json()
            self.SignalHttp.emit(r_dict)

