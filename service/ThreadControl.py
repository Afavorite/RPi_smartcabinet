import requests
from PyQt5.QtCore import QThread, pyqtSignal

import temp_get


class ThreadControl (QThread):
    SignalControl = pyqtSignal(list)
    control_list = []
    current_list = []

    def __init__(self):
        super().__init__()
        self.control_list = ['lock', 'off']
        self.current_list = ['lock', 'off']

    def run(self):
        while True:
            if self.control_list[0] != self.current_list[0]:
                if self.control_list[0] == 'lock':
                    print('关闭门锁')
                else:
                    print('开启门锁')
                self.current_list[0] = self.control_list[0]
            if self.control_list[1] != self.current_list[1]:
                if self.control_list[1] == 'on':
                    print('开启紫外线灯')
                else:
                    print('关闭紫外线灯')
                self.current_list[1] = self.control_list[1]