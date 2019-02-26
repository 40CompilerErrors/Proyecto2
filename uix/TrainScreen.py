from tkinter import *
from tkinter.filedialog import askdirectory

from uix import MainScreen as MS
from uix import TrainingResultScreen as TRS
from ETL import Trainer
from ETL import Models

class TrainController():

    def handle_event(self, window, command, **kwargs):
        if command == "EXIT":
            self.exit(window)
        elif command == "BACK":
            self.goto_previous(window)
        elif command == "SELECT_PATH":
            if 'label' in kwargs:
                self.select_path(window, label=kwargs.get('label'))
            else:
                print("ERROR: Needs a parameter \"label\"")
        elif command == "SELECT_MODEL":
            self.load_model_list(window)
        elif command == "START_TRAINING":
            self.start_training(window)
        else:
            print("Unrecognized command %s" % command)

    def exit(self, window):
        print("TODO implement exit")

    def goto_previous(self, window):
        window.root.remove_frame()
        MS.MainScreen(window.root)

    def select_path(self, window, label):
        folder = askdirectory()
        if label == "Good":
            window.selectGood_entry.delete(0, END)
            window.selectGood_entry.insert(END, folder)
        elif label == "Neutral":
            window.selectNeutral_entry.delete(0, END)
            window.selectNeutral_entry.insert(END, folder)
        elif label == "Bad":
            window.selectBad_entry.delete(0, END)
            window.selectBad_entry.insert(END, folder)
        else:
            print("Path not found!")
        print(folder)

    def load_model_list(self, window):
        chosen_model = window.modelVar.get()
        algorithm_list = Models.CHOICES_DICT[chosen_model]
        menu = window.popupMenu1["menu"]

        menu.delete(0, END)
        for algorithm in algorithm_list:
            menu.add_command(label=algorithm, command=lambda value=algorithm: window.modelVar1.set(value))

        window.modelVar1.set(algorithm_list[0])

        
    def start_training(self, window):

        # Code for training goes here
        path_label_good = window.selectGood_entry.get()
        print(path_label_good)
        path_label_neutral = window.selectNeutral_entry.get()
        print(path_label_neutral)
        path_label_bad= window.selectBad_entry.get()
        print(path_label_bad)

        if path_label_neutral and path_label_good and path_label_bad:
            model, vectorizer = Trainer.train(path_label_good,path_label_neutral,path_label_bad,
                                window.modelVar.get(),window.modelVar1.get())
            #Change window
            window.root.remove_frame()
            TRS.TrainingResultScreen(window.root, model, vectorizer)
        else:
            print(f"ERROR: Unvalid path or paths \n{path_label_good}\n{path_label_neutral}\n{path_label_bad}")




class TrainScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master

        self.exit_Frame = Frame(self.root, padx=10, pady=10, bg='#cbccd1')

        self.controller = TrainController()

        def send_event(command, **kwargs):
            self.controller.handle_event(self, command, **kwargs)

        # self.exit_btn = Button(self.exit_Frame, text='Exit', padx=5, pady=5, command=lambda: send_event("EXIT"))
        self.myImg4 = PhotoImage(file='resources/BackButton.png')
        self.back_btn = Button(self.exit_Frame, image=self.myImg4, command=lambda: send_event("BACK"))
        self.back_btn.configure(bg='#cbccd1', highlightthickness = 0, bd = 0)
        # self.exit_btn.config(relief='groove')
        # self.exit_btn.pack(side='right', fill="both", expand=True)
        self.back_btn.pack(side='right', fill="both", expand=True)

        # some tittle Frame ---------------------------------------------------------------------->
        self.title_Frame = Frame(self.root, bg='#cbccd1')

        self.someTitle_lbl = Label(self.title_Frame, text='Select Data and Model', bg='#cbccd1')
        self.someTitle_lbl.config(font=("Courier", 34))
        self.someTitle_lbl.pack()

        # Select Path Frame ---------------------------------------------------------------------->
        self.selectPath_Frame = Frame(self.root)
        self.selectPath_Frame.config(bg='#cbccd1')#cbccd1
        # self.center_Canvas = Canvas(self.selectPath_Frame, bg='#b8b8b8')
        # self.center_Canvas.pack()

        self.selectPathTable_Frame = Frame(self.selectPath_Frame)
        self.selectPathTable_Frame.pack(fill=BOTH, pady=100)
        # Good - Neutral - Bad icons
        self.myImgHappy = PhotoImage(file='resources/GoodIcon.png')
        self.imgModelHappy_lbl = Label(self.selectPathTable_Frame, image=self.myImgHappy)
        self.imgModelHappy_lbl.config(bg='#eaeaea')

        self.myImgNeutral = PhotoImage(file='resources/NeutralIcon.png')
        self.imgModelNeutral_lbl = Label(self.selectPathTable_Frame, image=self.myImgNeutral)
        self.imgModelNeutral_lbl.config(bg='#eaeaea')

        self.myImgSad = PhotoImage(file='resources/BadIcon.png')
        self.imgModelSad_lbl = Label(self.selectPathTable_Frame, image=self.myImgSad)
        self.imgModelSad_lbl.config(bg='#eaeaea')
        # Path Entry + button
        self.selectGood_entry = Entry(self.selectPathTable_Frame, justify='left')
        self.selectButton_btn = Button(self.selectPathTable_Frame, text='Select Path',
                                       command=lambda: send_event("SELECT_PATH", label="Good"))

        self.selectNeutral_entry = Entry(self.selectPathTable_Frame, justify='left')
        self.selectButton1_btn = Button(self.selectPathTable_Frame, text='Select Path',
                                        command=lambda: send_event("SELECT_PATH", label="Neutral"))

        self.selectBad_entry = Entry(self.selectPathTable_Frame, justify='left')
        self.selectButton2_btn = Button(self.selectPathTable_Frame, text='Select Path',
                                        command=lambda: send_event("SELECT_PATH", label="Bad"))
        # Grid Location
        self.imgModelHappy_lbl.grid(row=0, column=0, rowspan=2, pady=5, sticky=N + S + W + E)
        self.imgModelNeutral_lbl.grid(row=2, column=0, rowspan=2, pady=5, sticky=N + S + W + E)
        self.imgModelSad_lbl.grid(row=4, column=0, rowspan=2, pady=5, sticky=N + S + W + E)
        self.selectGood_entry.grid(row=0, column=1, padx=35, ipadx=200, sticky=N)
        self.selectNeutral_entry.grid(row=2, column=1, padx=35, ipadx=200, sticky=N)
        self.selectBad_entry.grid(row=4, column=1, padx=35, ipadx=200, sticky=N)
        self.selectButton_btn.grid(row=1, column=1, padx=35, sticky=W)
        self.selectButton1_btn.grid(row=3, column=1, padx=35, sticky=W)
        self.selectButton2_btn.grid(row=5, column=1, padx=35, sticky=W)

        # Select Model Frame ---------------------------------------------------------------------->
        self.selectModel_Frame = Frame(self.root)

        self.selectModelGrid_Frame = Frame(self.selectModel_Frame)
        self.selectModelGrid_Frame.pack(side='left', anchor='n')
        # img left Frame
        self.myImgModel = PhotoImage(file='resources/ModelIcon.png')
        self.imgModel_lbl = Label(self.selectModelGrid_Frame, image=self.myImgModel)
        # self.imgModel_lbl.pack(fill="both", expand=True)
        self.imgModel_lbl.config(bg='#eaeaea')
        # entry + select btn right Frame
        self.modelVar = StringVar()
        self.modelVar1 = StringVar()

        model_list = Models.CHOICES_DICT

        self.modelVar.set(next(iter(model_list)))
        print(model_list[self.modelVar.get()])
        # self.modelVar.trace('w', self.CHOICES_DICT[self.modelVar.get()])
        self.popupMenu = OptionMenu(self.selectModel_Frame, self.modelVar, *model_list,
                                    command=lambda needsanameforsomereason: send_event("SELECT_MODEL"))
        self.popupMenu1 = OptionMenu(self.selectModel_Frame, self.modelVar1, *model_list[self.modelVar.get()])
        send_event("SELECT_MODEL")

        # self.selectModel_lbl = Label(self.selectModel_Frame, text='Chose a Model')
        # self.selectModel_entry = Entry(self.selectModelGrid_Frame, justify='right')
        # self.selectModel_btn = Button(self.selectModelGrid_Frame, text='Select Model',
        #                               command=lambda: send_event("SELECT_MODEL"))
        # Grid location
        self.imgModel_lbl.pack(side=LEFT)
        self.popupMenu.pack(side=TOP, padx=10)
        self.popupMenu1.pack(side=LEFT, padx=10)
        # self.selectModel_lbl.pack(side=TOP, padx=10)


        # start training Button Frame ---------------------------------------------------------------------->
        self.startTraining_Frame = Frame(self.root)
        self.myImg1 = PhotoImage(file='resources/StartTrainingButton.png')
        self.startTraining_btn = Button(self.startTraining_Frame, image=self.myImg1, padx=10, pady=10,
                                        command=lambda: send_event("START_TRAINING"))
        self.startTraining_btn.configure(highlightthickness = 0, bd = 0)
        self.startTraining_btn.pack()

        # position of the mainData frames into the grid ---------------------------------------------------------------------->
        self.exit_Frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=E)
        self.title_Frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.selectPath_Frame.grid(row=2, column=0, columnspan=2, padx=75, sticky=N + S)
        self.selectModel_Frame.grid(row=3, column=0, padx=85, pady=65, sticky=W)
        self.startTraining_Frame.grid(row=3, column=1, padx=85, pady=65, sticky=E)

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.root.mainloop()

    def get_model_menu(self):
        return self.modelVar
