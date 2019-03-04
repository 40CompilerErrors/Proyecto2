import main as m
from Views import MainMenu as MM
from Model import Classifiers, Trainer
from tkinter.filedialog import askdirectory

class AdminController:

    def __init__(self, view):
        self.view = view

    def train_classifier(self):

        key1, key2 = self.__select_model()
        path_good, path_neutral, path_bad = self.__get_paths()

        model, vectorizer = Trainer.train(path_good, path_neutral, path_bad, key1, key2)

        self.__save_model(model,vectorizer)
        self.__ask_quit()

    def go_back(self):
        self.view.running = False
        m.current = MM.MainMenu()


    #Private Methods (AKA Magic)


    def __select_model(self):
        key1_list = []
        key1 = ""

        key2_list = []
        key2 = ""

        #Choose the First Key
        for model in Classifiers.CHOICES_DICT:
            key1_list.append(model)
        running = True

        while running:
            print("Select one of the Following models:")

            for i in range(len(key1_list)):
                print(str(i) + " - " + key1_list[i])

            user_input = input()

            #check if out of bounds
            if int(user_input) < 0 or int(user_input) >= len(key1_list):
                print("Number out of bounds\n")
            else:
                running = False;
                key1 = key1_list[int(user_input)]



        #Choose the Second Key
        for model in Classifiers.CHOICES_DICT[key1]:
            key2_list.append(model)

        running = True

        while running:
            print("You have chosen to train a " + key1)
            print("Now choose one of the more specific types for this model:")

            for i in range(len(key2_list)):
                print(str(i) + " - " + key2_list[i])

            user_input = input()

            # check if out of bounds
            if int(user_input) < 0\
                    or int(user_input) >= len(key2_list):
                print("Number out of bounds\n")
            else:
                running = False;
                key2 = key2_list[int(user_input)]


        print(key1 + " " + key2)
        return key1, key2


    def __get_paths(self):

        print("Choose a path for GOOD reviews")
        path_good = askdirectory()

        print("Choose a path for NEUTRAL reviews")
        path_neutral = askdirectory()

        print("Choose a path for BAD reviews")
        path_bad = askdirectory()

        return path_good, path_neutral, path_bad

    def __save_model(self, model, vectorizer):

        running = True
        while running:

            print("Do you wish to save the model? Y/N")

            user_input = input();

            if user_input == "Y" or user_input == "y":
                print("Select a directory to save the model and vocab")
                save_to = askdirectory()

                print("Give a name to the model and vocav (They share name, but not extension)")
                user_input = input()

                self.model.export_model(save_to, user_input)
                self.vectorizer.export_vectorizer(save_to, user_input)

                print("Saved model and vocab successfully")
                running = False
            elif user_input == "N" or user_input == "n":
                running = False
            else:
                print("Invalid Command\n")


    def __ask_quit(self):
        running = True
        while running:

            print("Do you wish to quit? Y/N")
            user_input = input();
            if user_input == "Y" or user_input == "y":
                running = False
                self.view.running = False
            elif user_input == "N" or user_input == "n":
                running = False
            else:
                print("Invalid Command \n")
