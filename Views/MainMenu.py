import sys
from Controllers import MainController as MC


class MainMenu:

    def __init__(self):

        self.controller = MC.MainController(self)
        running = True

        while running:

            print("Who do you want to log in as?")
            print("1 - User")
            print("2 - Administrator")
            print("X - Exit")

            user_input = input();


            if user_input == "1":
                self.controller.user_access("user","")
            elif user_input == "2":
                self.controller.user_access("admin","")
            elif user_input == "X" or user_input == "x":
                sys.exit(0)
            else:
                print("\nThat command does not exist.\n")
