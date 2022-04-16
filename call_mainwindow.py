from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import *
from ui.mainwindow import Ui_Form
from service.ThreadHttp import ThreadHttp

import temp_get


class MainPageWindow(QWidget, Ui_Form):
    # MainPageWindow继承自mainwindow.Ui_Form，实现UI和逻辑之间的分离

    def __init__(self, parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.thread_conn = ThreadHttp()
        self.timer_show = QTimer()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # Http连接线程
        self.thread_conn.Signal.connect(self.receive)
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

    def receive(self, r_list):
        if r_list:
            # box_list = [item[key] for item in r_list for key in item]
            # print(box_list)
            self.label_displaystatus.setText('当前用户：' + r_list[0]['order_creator'])
        else:
            self.label_displaystatus.setText('当前无用户')
