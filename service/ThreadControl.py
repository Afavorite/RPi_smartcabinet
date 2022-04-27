import time
from threading import Thread
from time import sleep

import requests
from PyQt5.QtCore import QThread, pyqtSignal
import RPi.GPIO as GPIO

import temp_get


class ThreadControl(QThread):
    SignalControl = pyqtSignal(dict)
    order_temp = ''  # 初始化温控
    order_ster = ''  # 初始化紫外线灯
    order_lock = ''  # 初始化门锁

    IN_ster = 5
    IN_lock = 6
    IN_lock_feedback = 12

    flag = False
    controlfb = {}

    def __init__(self):
        super().__init__()
        self.order_temp = 'stop'  # 初始化温控
        self.order_ster = 'off'
        self.order_lock = 'lock'
        self.controlfb = {'ster': 'off', 'lock': 'lock'}

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN_ster, GPIO.OUT)
        GPIO.setup(self.IN_lock, GPIO.OUT)
        GPIO.setup(self.IN_lock_feedback, GPIO.IN)# , pull_up_down=GPIO.PUD_DOWN)
        # 侦测到关门信号，进入中断函数
        # GPIO.add_event_detect(self.IN_lock_feedback, GPIO.RISING, callback=self.lock_callback, bouncetime=200)
        GPIO.add_event_detect(self.IN_lock_feedback, GPIO.RISING)

    def run(self):
        # controlfb = {}
        while True:
            if self.order_ster == 'on':
                GPIO.output(self.IN_ster, True)
                self.controlfb['ster'] = 'on'

            if self.order_ster == 'off':
                GPIO.output(self.IN_ster, False)
                self.controlfb['ster'] = 'off'
            time.sleep(0.75)

            if GPIO.event_detected(self.IN_lock_feedback):
                print('门锁已关闭')
                self.flag = True
                self.controlfb['lock'] = 'lock'
                t = Thread(target=self.timewait)
                t.start()

            if self.order_lock == 'unlock' and self.controlfb['lock'] == 'lock' and self.flag is False:
                sleep(0.5)
                if self.order_lock == 'unlock' and self.controlfb['lock'] == 'lock' and self.flag is False:
                    self.controlfb['lock'] = 'unlock'
                    print('门锁通电')
                    GPIO.output(self.IN_lock, True)
                    # GPIO.remove_event_detect(self.IN_lock_feedback)
                    time.sleep(1)
                    print('门锁断电')
                    GPIO.output(self.IN_lock, False)
                    # time.sleep(1)
                    # GPIO.add_event_detect(self.IN_lock_feedback, GPIO.RISING)

            self.SignalControl.emit(self.controlfb)

    # 防止门锁关闭后，由于指令的延时导致门锁再次打开
    # def lock_callback(self, IN_lock_feedback):
    #     print('门锁已关闭')
    #     self.flag = True
    #     self.controlfb['lock'] = 'lock'
    #     t = Thread(target=self.timewait)
    #     t.start()

    # 延时一段时间，保证服务器收到门锁已关闭的信号，并修改指令
    # def timewait(self):
    #     sleep(3)
    #     self.flag = False
