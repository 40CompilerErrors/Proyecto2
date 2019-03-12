from Views import MainMenu as MM
import sys
from PyQt5.QtWidgets import QApplication

class Main:

    def __init__(self):
        app = QApplication(sys.argv)
        self.__change_current(MM.MainMenu())
        sys.exit(app.exec_())

    def __change_current(self,window):
        self.current= window
        self.current.show()

if __name__ == "__main__":
    # execute only if run as a script
    Main()
