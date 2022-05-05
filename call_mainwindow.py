from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import *
from ui.mainwindow import Ui_Form
from service.ThreadHttp import ThreadHttp
from service.ThreadControl import ThreadControl, ThreadTemp, IncrementalPID

import temp_get


class MainPageWindow(QWidget, Ui_Form):
    # MainPageWindow继承自mainwindow.Ui_Form，实现UI和逻辑之间的分离
    # signaltocontrol = pyqtSignal(list)
    # signaltohttp = pyqtSignal(list)

    def __init__(self, parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.thread_temp = ThreadTemp()
        self.thread_conn = ThreadHttp()
        self.thread_control = ThreadControl()
        # self.thread_temp = ThreadTemp()
        self.timer_show = QTimer()
        self.setupUi(self)
        self.initUI()
        self.tempflag = 0

    def initUI(self):
        # 紫外线灯和门锁控制线程
        self.thread_control.SignalControl.connect(self.receiveControl)
        self.thread_control.start()
        # Http连接线程
        self.thread_conn.SignalHttp.connect(self.receiveHttp)
        self.thread_conn.start()
        # 设置定时器，刷新显示
        temp_get.setup()
        self.timer_show.timeout.connect(self.display)  # 这个通过调用槽函数来刷新显示
        self.timer_show.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms

    def display(self):
        time = QDateTime.currentDateTime()  # 获取当前时间
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss")  # 格式化一下时间
        self.label_displaytime.setText(timedisplay)

        temperature = temp_get.read()
        self.label_displaytemp.setText('当前温度：' + str(round(temperature, 2)) + '℃')

    def receiveHttp(self, r_dict):
        if r_dict['control_flag'] == 'booking':
            self.label_displaytempswitch.setText('温控已关闭')
            if self.thread_temp.isRunning():
                self.tempflag = 0
                self.thread_temp.canrun = False
                print('温控关闭')
            self.thread_control.order_ster = 'off'
            self.thread_control.order_lock = 'lock'
            self.label_displaystatus.setText('箱柜已被预约')

        if r_dict['control_flag'] == 'using':
            if r_dict['control_temp'] != 'stop' and self.tempflag == 0:
                self.tempflag = 1
                self.thread_temp.canrun = True
                self.thread_temp.start()
                self.label_displaytempswitch.setText('温控已打开')

            self.thread_control.order_ster = r_dict['control_ster']
            self.thread_control.order_lock = 'lock'
            self.label_displaystatus.setText('箱柜使用中')

        if r_dict['control_flag'] == 'unlock':
            self.label_displaytempswitch.setText('温控已关闭')
            if self.thread_temp.isRunning():
                self.tempflag = 0
                self.thread_temp.canrun = False
                print('温控关闭')
            self.thread_control.order_ster = 'off'
            self.thread_control.order_lock = 'unlock'
            self.label_displaystatus.setText('箱柜已解锁')

        if r_dict['control_flag'] == 'finish':
            # self.thread_control.order_temp = 'stop'
            self.label_displaytempswitch.setText('温控已关闭')
            if self.thread_temp.isRunning():
                self.tempflag = 0
                self.thread_temp.canrun = False
                print('温控关闭')
            self.thread_control.order_ster = 'off'
            self.thread_control.order_lock = 'lock'
            self.label_displaystatus.setText('箱柜空闲')

    def receiveControl(self, controlfb):
        self.thread_conn.lock = controlfb['lock']
        self.thread_conn.ster = controlfb['ster']
        # if controlfb['lock'] == 'lock':
        #     self.label_displaylock.setText('门锁已经关闭')
        # else:
        #     self.label_displaylock.setText('门锁已经打开')
        if controlfb['ster'] == 'on':
            self.label_displayster.setText('紫外线灯打开')
        else:
            self.label_displayster.setText('紫外线灯关闭')

