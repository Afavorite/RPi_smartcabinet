import time
from time import sleep

import requests
from PyQt5.QtCore import QThread, pyqtSignal
import RPi.GPIO as GPIO

import temp_get


class ThreadControl (QThread):
    SignalControl = pyqtSignal(dict)
    order_temp = ''# 初始化温控
    order_ster = ''# 初始化紫外线灯
    order_lock = ''# 初始化门锁

    IN_ster = 5
    IN_lock = 6
    IN_lock_feedback = 12

    def __init__(self):
        super().__init__()
        self.order_temp = 'stop'  # 初始化温控
        self.order_ster = 'off'
        self.order_lock = 'lock'
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN_ster, GPIO.OUT)
        GPIO.setup(self.IN_lock, GPIO.OUT)
        GPIO.setup(self.IN_lock_feedback, GPIO.IN)

    def run(self):
        while True:
            controlfb = {}
            if self.order_ster == 'on':
                GPIO.output(self.IN_ster, True)
                controlfb['ster'] = 'on'

            if self.order_ster == 'off':
                GPIO.output(self.IN_ster, False)
                controlfb['ster'] = 'off'
            time.sleep(1)

            # if self.order_lock == 'unlock' and GPIO.input(self.IN_lock_feedback) == GPIO.HIGH:
            #     GPIO.output(self.IN_lock, True)
            #     time.sleep(0.5)
            #     GPIO.output(self.IN_lock, False)
            #     controlfb['lock'] = 'unlock'
            # if GPIO.input(self.IN_lock_feedback) != GPIO.HIGH:  # 检测到柜门已打开
            #     controlfb['lock'] = 'unlock'
            # if GPIO.input(self.IN_lock_feedback) == GPIO.HIGH:
            #     controlfb['lock'] = 'lock'

            self.SignalControl.emit(controlfb)
    # def settemp(self, order_temp):
    #     self.order_temp = order_temp
    #
    # def setster(self, order_ster):
    #     self.order_ster = order_ster
    #
    # def setlock(self, order_lock):
    #     self.order_lock = order_lock
