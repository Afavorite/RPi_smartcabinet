import sys
import ui.window
from call_mainwindow import MainPageWindow
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    app = QApplication(sys.argv)

    m = MainPageWindow()
    # 实例ui
    # UI = ui.window.Ui_Form()
    # 主窗口添加控件
    # UI.setupUi(m)

    m.show()
    sys.exit(app.exec_())
