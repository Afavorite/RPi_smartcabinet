import sys
import ui.mainwindow
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    app = QApplication(sys.argv)
    m = QWidget()
    # 实例ui
    ui = ui.mainwindow.Ui_Form()
    # 主窗口添加控件
    ui.setupUi(m)
    m.show()
    sys.exit(app.exec_())
