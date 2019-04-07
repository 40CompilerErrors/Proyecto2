from Views import ClassifyMenu as CM
from Views import ClassifyWebMenu as CWM
class UserController:

    def __init__(self, view):
        self.view = view

    def openClass(self):
        window = CM.ClassifyMenu()
        window.show()

    def openWebClass(self):
        window = CWM.ClassifyWebMenu()
        window.show()





