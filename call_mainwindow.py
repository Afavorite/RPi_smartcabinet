from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import *
from ui.mainwindow import Ui_Form

from w1thermsensor import W1ThermSensor, Sensor


class MainPageWindow(QWidget,Ui_Form):
    # MainPageWindow继承自mainwindow.Ui_Form，实现UI和逻辑之间的分离
    float temperature
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
        # 设置定时器，刷新温度显示
        self.timer_gettemp = QTimer()
        self.timer_gettemp.timeout().connect(self.gettemp())
        self.timer_gettemp.start(1500)

    @PYQT_SLOT
    def showtime(self):
        time = QDateTime.currentDateTime()  # 获取当前时间
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss")  # 格式化一下时间
        # print(timedisplay)
        self.label_displaytime.setText(timedisplay)
    @PYQT_SLOT
    def showtemp(self):
        self.label_displaytemp.setText(str(round(temperature, 2)))

    def gettemp(self):
        sensor = W1ThermSensor(Sensor.DS18B20, "3c5ef648a81c")
        temperature = sensor.get_temperature()
        print(temperature)
