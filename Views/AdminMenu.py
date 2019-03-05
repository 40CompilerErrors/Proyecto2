from Controllers import AdminController as AC
from Model import Classifiers


class AdminMenu:

    def __init__(self):

        self.controller = AC.AdminController(self)

        running = True
        while running:

            print("What do you want to do?")
            print("1 - Train (Classifier)")
            print("X - Go Back")

            user_input = input();

            if user_input == "1":
                self.controller.train_classifier()
            elif user_input == "X" or user_input == "x":
                self.controller.go_back()
            else:
                print("\nThat command does not exist.\n")

