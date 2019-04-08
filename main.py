from Views import LoginMenu as MM
import sys
from PyQt5.QtWidgets import QApplication

class Main:

    def __init__(self):
        app = QApplication(sys.argv)
        self.change_current(MM.LoginMenu())
        sys.exit(app.exec_())

    def change_current(self,window):
        self.current= window
        self.current.show()

if __name__ == "__main__":
    # execute only if run as a script
    Main()
