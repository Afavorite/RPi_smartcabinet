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

            self.SignalControl.emit(self.controlfb)

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
    IN_PWM = 19
    settemp = '10'

    def __init__(self):
        super().__init__()
        print('温控初始化')
        temp_get.setup()

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN_PWM, GPIO.OUT)
        self.pwm = GPIO.PWM(self.IN_PWM, 100)

    def run(self):
        inc_pid = IncrementalPID(5.0, 0.2, 0.2)
        temp = float(self.settemp)
        self.pwm.start(100)
        while True:
            inc_pid.SetStepSignal(temp)
            # inc_pid.SetInertiaTime(3, 0.1)
            # print(inc_pid.PIDOutput)
            # print(inc_pid.SystemOutput)
            compare = inc_pid.PIDOutput - temp
            if compare > 10:
                inc_pid.PIDOutput = temp + 10
                compare = 10
            elif compare < 0:
                inc_pid.PIDOutput = temp
                compare = 0
            if temp - temp_get.read() > 1:
                self.pwm.ChangeDutyCycle(100)
            else:
                if 10 >= compare > 6:
                    self.pwm.ChangeDutyCycle(100)
                elif 6 >= compare > 3:
                    self.pwm.ChangeDutyCycle(50)
                elif 3 >= compare > 2:
                    self.pwm.ChangeDutyCycle(40)
                elif 2 >= compare > 1:
                    self.pwm.ChangeDutyCycle(30)
                elif 1 >= compare > 0.5:
                    self.pwm.ChangeDutyCycle(20)
                else:
                    self.pwm.ChangeDutyCycle(0)
            # print(compare)
            sleep(1)
            if self.canrun is False:
                self.pwm.stop()
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
        self.LastLastError = self.LastError
        self.LastError = self.Error

    # 以一阶惯性环节为例子演示控制效果
    def SetInertiaTime(self, IntertiaTime, SampleTime):
        self.SystemOutput = (IntertiaTime * self.LastSystemOutput + SampleTime * self.PIDOutput) / (
                    SampleTime + IntertiaTime)
        self.LastSystemOutput = self.SystemOutput

