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
    # IN_UP = 13
    # IN_DOWN = 16

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
        GPIO.setup(self.IN_lock_feedback, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # 侦测到关门信号，进入中断函数
        # GPIO.add_event_detect(self.IN_lock_feedback, GPIO.RISING, callback=self.lock_callback, bouncetime=200)
        # GPIO.add_event_detect(self.IN_lock_feedback, GPIO.RISING, bouncetime=200)

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

            # if GPIO.event_detected(self.IN_lock_feedback):
            #     # print('门锁已关闭')
            #     self.flag = True
            #     self.controlfb['lock'] = 'lock'
            #     t = Thread(target=self.timewait)
            #     t.start()

            # if GPIO.input(self.IN_lock_feedback):
            #     print('高电平')
            # else:
            #     print('低电平')
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
                    t = Thread(target=self.lock_check)
                    t.start()
                    # time.sleep(1)
                    # GPIO.add_event_detect(self.IN_lock_feedback, GPIO.RISING, callback=self.lock_callback, bouncetime=200)

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
    #     sleep(5)
    #     self.flag = False

    def lock_check(self):
        print('开锁')
        while GPIO.input(self.IN_lock_feedback) == 0:
            sleep(0.5)
        print('关锁')
        self.flag = True
        self.controlfb['lock'] = 'lock'
        sleep(5)
        self.flag = False


class ThreadTemp(QThread):
    canrun = True
    # temp_get.setup()

    def __init__(self):
        super().__init__()
        print('温控初始化')

    def run(self):
        inc_pid = IncrementalPID(5.0, 0.2, 0.1)
        while True:
            inc_pid.SetStepSignal(30.0)
            print(inc_pid.PIDOutput)
            sleep(0.5)
            if self.canrun is False:
                return


class IncrementalPID:
    def __init__(self, P: float, I: float, D: float):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.PIDOutput = 0.0  # PID控制器输出
        self.SystemOutput = 0.0  # 系统输出值
        self.LastSystemOutput = 0.0  # 系统的上一次输出

        self.Error = 0.0
        self.LastError = 0.0
        self.LastLastError = 0.0

        temp_get.setup()

    # 设置PID控制器参数
    def SetStepSignal(self, StepSignal):
        # self.Error = StepSignal - self.SystemOutput
        self.Error = StepSignal - temp_get.read()
        # 计算增量
        IncrementalValue = self.Kp * (self.Error - self.LastError) \
                           + self.Ki * self.Error + self.Kd * (self.Error - 2 * self.LastError + self.LastLastError)
        # 计算输出
        self.PIDOutput += IncrementalValue
        print(self.PIDOutput)
        self.LastLastError = self.LastError
        self.LastError = self.Error

    # 以一阶惯性环节为例子演示控制效果
    # def SetInertiaTime(self, IntertiaTime, SampleTime):
    #     self.SystemOutput = (IntertiaTime * self.LastSystemOutput + SampleTime * self.PIDOutput) / (
    #                 SampleTime + IntertiaTime)
    #     self.LastSystemOutput = self.SystemOutput

