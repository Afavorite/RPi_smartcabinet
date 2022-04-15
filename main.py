import sys
from call_mainwindow import MainPageWindow
from PyQt5.QtWidgets import QApplication, QWidget
from service.ThreadHttp import ThreadHttp

if __name__ == '__main__':

    app = QApplication(sys.argv)
    m = MainPageWindow()
    m.show()

    thread_conn = ThreadHttp()
    thread_conn.start()


    sys.exit(app.exec_())
