from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import *
from ui.mainwindow import Ui_Form

from w1thermsensor import W1ThermSensor, Sensor

import temp_get


class MainPageWindow(QWidget, Ui_Form):
    # MainPageWindow继承自mainwindow.Ui_Form，实现UI和逻辑之间的分离
    def __init__(self, parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 设置定时器，刷新显示
        self.timer_show = QTimer()
        self.timer_show.timeout.connect(self.showtime)  # 这个通过调用槽函数来刷新时间
        self.timer_show.timeout.connect(self.showtemp)  # 这个通过调用槽函数来刷新温度
        self.timer_show.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms

    def showtime(self):
        time = QDateTime.currentDateTime()  # 获取当前时间
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss")  # 格式化一下时间
        # print(timedisplay)
        self.label_displaytime.setText(timedisplay)

    def showtemp(self):
        temp_get.setup()
        temperature = temp_get.read()
        self.label_displaytemp.setText('当前温度：' + str(round(temperature, 2)) + '℃')
