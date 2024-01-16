
from jsonEditUI import *
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys

class Main(QMainWindow, Json_Edit):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(self.win_icon)
        self.setWindowTitle('Json编辑器\t\t')
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Exe = Main()
    Exe.show()
    sys.exit(app.exec_())
