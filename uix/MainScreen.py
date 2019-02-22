from tkinter import *

from proyecto_1.uix import ClassifyScreen as CS
from proyecto_1.uix import TrainScreen as TS


class MainController():

    def handle_event(self, window, command, **kwargs):
        if command == "EXIT":
            self.exit(window)
        elif command == "HELP":
            self.goto_help()
        elif command == "CLASSIFY":
            self.goto_classify(window)
        elif command == "TRAINING":
            self.goto_training(window)
        else:
            print("Unrecognized command %s" % command)

    def exit(self, window):
        print("TODO implement exit")

    def goto_help(self):
        print("TODO: Implement goto_help")

    def goto_training(self, window):
        window.root.remove_frame()
        TS.TrainScreen(window.root)

    def goto_classify(self, window):
        window.root.remove_frame()
        CS.ClassifyScreen(window.root)


class MainScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master

        self.exit_Frame = Frame(self.root, padx=10, pady=10, bg='#cbccd1')

        self.controller = MainController()

        def send_event(command):
            self.controller.handle_event(self, command)

        # help-exit Frame
        self.exit_Frame = Frame(self.root, bg='#dfdfdf')

        # self.exit_btn = Button(self.exit_Frame, text='Exit', padx=5, pady=5, command=lambda: send_event("EXIT"))
        self.myImg5 = PhotoImage(file='resources/HelpButton.png')
        self.help_btn = Button(self.exit_Frame, image=self.myImg5, command=lambda: send_event("HELP"))
        self.help_btn.configure(highlightthickness = 0, bd = 0)
        # self.exit_btn.config(relief='groove')
        # self.exit_btn.pack(side='right', fill="both", expand=True)
        #self.help_btn.pack(side='right', fill="both", expand=True)

        # img logo Frame
        self.logo_Frame = Frame(self.root, width=1000, height=800)

        self.myImg = PhotoImage(file='resources/logo.png')
        self.img_lbl = Label(self.logo_Frame, image=self.myImg)
        self.img_lbl.pack(fill="both", expand=True)
        self.img_lbl.config(bg='#cbccd1')

        # Three Dudes Inc. logo
        self.tdiName_Frame = Frame(self.root, bg='#cbccd1')

        self.tdiName_lbl = Label(self.tdiName_Frame, text='Three Dudes Inc.', bg='#cbccd1', pady=20)
        self.tdiName_lbl.config(font=("Courier", 34))
        self.tdiName_lbl.pack()

        # button Frame
        # self.btn_Frame = Frame(self.mainFrame)
        self.btn_left_Frame = Frame(self.root, width=150, height=150)
        self.btn_right_Frame = Frame(self.root, width=150, height=150)

        # self.btn_left_Frame.pack(side='left', fill="both", expand=True)
        # self.btn_right_Frame.pack(side='right', fill="both", expand=True)

        self.myImg1 = PhotoImage(file='resources/TrainingButton.png')
        self.entrenamiento_btn = Button(self.btn_left_Frame, image=self.myImg1, padx='5', pady='5',
                                        command=lambda: send_event("TRAINING"))
        self.myImg2 = PhotoImage(file='resources/ClassifyButton.png')
        self.clasificador_btn = Button(self.btn_right_Frame, image=self.myImg2, padx='5', pady='5',
                                       command=lambda: send_event("CLASSIFY"))
        # self.entrenamiento_btn = Button(self.btn_left_Frame, text='Entrenamiento',padx='10',pady='10')
        # self.clasificador_btn = Button(self.btn_right_Frame, text='Clasificador', padx='10', pady='10')
        self.entrenamiento_btn.pack()
        self.clasificador_btn.pack()

        # posicion de los mainFrame en el grid
        self.exit_Frame.grid(row=0, column=0, columnspan=2, sticky=E, padx=5, pady=5)
        self.logo_Frame.grid(row=1, column=0, columnspan=2, sticky=N + S + E + W)
        self.tdiName_Frame.grid(row=2, column=0, columnspan=2, sticky=N + S, padx=10, pady=10)
        self.btn_left_Frame.grid(row=3, column=0, sticky=W, padx=85, pady=115)
        self.btn_right_Frame.grid(row=3, column=1, sticky=E, padx=85, pady=115)

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.mainloop()
