import sys
from call_mainwindow import MainPageWindow
from PyQt5.QtWidgets import QApplication, QWidget
from service.ThreadHttp import ThreadHttp

if __name__ == '__main__':

    app = QApplication(sys.argv)
    m = MainPageWindow()
    m.showFullScreen()

    sys.exit(app.exec_())
