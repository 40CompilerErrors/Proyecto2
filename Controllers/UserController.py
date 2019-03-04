from Views import MainMenu as MM
import main as m
from tkinter.filedialog import askdirectory

class UserController:

    def __init__(self, view):
        self.view = view

    def go_back(self):
        self.view.running = False
        m.current = MM.MainMenu()

    def perform_classification(self):
        pass

    def perform_sentiment_analysis(self):
        print("Choose a path for the reviews to classify")
        path = askdirectory()

        #SENTIMENT ANALYSIS HERE