from Controllers import UserController as UC


class UserMenu:

    def __init__(self):

        self.controller = UC.UserController(self)
        running = True

        while running:

            print("What do you want to do?")
            print("1 - Classify")
            print("2 - Sentiment Analysis")
            print("X - Go Back")

            user_input = input();

            if user_input == "1":
                self.controller.perform_classification()
            elif user_input == "2":
                self.controller.perform_sentiment_analysis()
            elif user_input == "X" or user_input == "x":
                self.controller.go_back()
            else:
                print("\nThat command does not exist.\n")