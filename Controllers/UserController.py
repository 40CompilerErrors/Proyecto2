from Views import MainMenu as MM
import main as m
from tkinter.filedialog import askdirectory, askopenfilename
from Model import File_Manager, Vectorizer, Classifiers

class UserController:

    def __init__(self, view):
        self.view = view

    def go_back(self):
        self.view.running = False
        m.current = MM.MainMenu()

    def perform_classification(self):

        unlabeled_path = self.__select_unlabeled_path()
        model_path, vocab_path = self.__select_unlabeled_path()
        model, vectorizer, x_unlabeled = self.__load_model(unlabeled_path,model_path,vocab_path)

        prediction = model.predict(x_unlabeled)
        print(prediction)

        self.__export_to_csv(vectorizer)
        self.__ask_quit()


    def perform_sentiment_analysis(self):
        print("Choose a path for the reviews to classify")
        path = askdirectory()

        #SENTIMENT ANALYSIS HERE
        print(" UNIMPLEMENTED")




    #PRIVATE METHODS



    def __select_unlabeled_path(self):
        print("Choose a path for the reviews to classify")
        unlabeled_path = askdirectory()

        return unlabeled_path


    def __select_model(self):
        print("Select a model to use")
        model_path = askopenfilename()

        print("Select the model's vocabulary")
        vocab_path = askopenfilename()

        return model_path, vocab_path


    def __load_model(self,unlabeled_path,model_path,vocab_path):
        fm = File_Manager.File_Manager()
        unlabeled_reviews, u_file_names = fm.extract_data_from_files(self.unlabeled_path)
        vectorizer = Vectorizer.Vectorizer(u_reviews=unlabeled_reviews)
        vectorizer.load_vectorizer(self.vocab_path)
        x_unlabeled = vectorizer.generate_unlabeled_data(u_file_names)
        model = Classifiers.Models()
        model.load_model(self.model_path)

        return model, vectorizer, x_unlabeled

    def __export_to_csv(self,vectorizer):

        running = True;
        while running:

            print("Do you want to save the results to CSV? Y/N")

            user_input = input();

            if user_input == "Y" or user_input == "y":
                print("Introduce a path to save to")
                path = askdirectory()
                vectorizer.export_dataframe_csv(path=path, model_name='summary')
                print("Results saved successfully")
                running = False;
            elif user_input == "N" or user_input == "n":
                running = False
            else:
                print("\nThat command does not exist.\n")

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