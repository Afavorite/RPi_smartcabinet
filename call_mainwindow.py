from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime, pyqtSignal
from PyQt5.QtWidgets import *
from ui.mainwindow import Ui_Form
from service.ThreadHttp import ThreadHttp
from service.ThreadControl import ThreadControl

import temp_get


class MainPageWindow(QWidget, Ui_Form):
    # MainPageWindow继承自mainwindow.Ui_Form，实现UI和逻辑之间的分离
    # signaltocontrol = pyqtSignal(list)
    # signaltohttp = pyqtSignal(list)

    def __init__(self, parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.thread_conn = ThreadHttp()
        # self.thread_control = ThreadControl()
        self.timer_show = QTimer()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 紫外线灯和门锁控制线程
        # self.thread_control.SignalControl.connect(self.receiveControl)
        # self.thread_control.start()
        # Http连接线程
        # self.thread_conn.SignalHttp.connect(self.receiveHttp)
        self.thread_conn.start()
        # 设置定时器，刷新显示
        self.timer_show.timeout.connect(self.display)  # 这个通过调用槽函数来刷新显示
        self.timer_show.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms

    def display(self):
        time = QDateTime.currentDateTime()  # 获取当前时间
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss")  # 格式化一下时间
        self.label_displaytime.setText(timedisplay)

        temp_get.setup()
        temperature = temp_get.read()
        self.label_displaytemp.setText('当前温度：' + str(round(temperature, 2)) + '℃')

    # def receiveHttp(self, r_list):
    #     if r_list:
    #         self.label_displaystatus.setText('当前用户：' + r_list[0]['order_creator'])
    #         lock = r_list[0]['order_status']
    #         if lock != "unlock":
    #             lock = 'lock'
    #         else:
    #             lock = 'unlock'
    #         ster = r_list[0]['order_sterilization']
    #         control_list = [lock, ster]
    #         self.thread_control.control_list = control_list
    #         # self.signaltocontrol.emit(control_list)
    #     else:
    #         self.label_displaystatus.setText('当前无用户')

    # def receiveControl(self):
