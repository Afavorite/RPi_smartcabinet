from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import *
from ui.mainwindow import Ui_Form

class MainPageWindow(QWidget,Ui_Form):
    # MainPageWindow继承自mainwindow.Ui_Form，实现UI和逻辑之间的分离
    def __init__(self, parent=None):
        super(MainPageWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        #
        self.timer = QTimer()
        self.timer.timeout.connect(self.showtime)  # 这个通过调用槽函数来刷新时间
        self.timer.start(1000)  # 每隔一秒刷新一次，这里设置为1000ms

    def showtime(self):
        time = QDateTime.currentDateTime()  # 获取当前时间
        timedisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")  # 格式化一下时间
        # print(timedisplay)
        self.label_displaytime.setText(timedisplay)