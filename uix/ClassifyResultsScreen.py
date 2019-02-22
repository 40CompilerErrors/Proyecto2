from tkinter import *
from tkinter import ttk
import os

from proyecto_1.uix import MainScreen as MS
from proyecto_1.uix import TrainScreen as TS
from proyecto_1.ETL import Models
from tkinter.filedialog import askdirectory,asksaveasfilename

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



class ClassifyResultsController:

    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    def handle_event(self, window, command, **kwargs):
        if command == "EXIT":
            self.exit(window)
        elif command == "BACK":
            self.goto_previous(window)
        elif command == "EXPORT_TO_CSV":
            self.export_to_csv()
        elif command == "EXPORT_TO_FOLDERS":
            self.export_to_folders()
        else:
            print("Unrecognized command %s" % command)

    def exit(self, window):
        print("TODO implement exit")

    def goto_previous(self, window):
        window.root.remove_frame()
        TS.TrainScreen(window.root)

    def goto_main_menu(self, window):
        window.root.remove_frame()
        MS.MainScreen(window.root)

    def export_to_csv(self):
        path = askdirectory()
        self.vectorizer.export_dataframe_csv(path=path, model_name='summary')
        print("exportado correctamente")
        pass

    def export_to_folders(self):
        path = askdirectory()
        self.vectorizer.export_reviews_to_files(path)
        print('exportado correctamente')


class ClassifyResultsScreen(Frame):
    def __init__(self, master, vectorizer):
        Frame.__init__(self, master)
        self.root = master

        self.exit_Frame = Frame(self.root, padx=10, pady=10, bg='#cbccd1')

        self.controller = ClassifyResultsController(vectorizer)

        def send_event(command):
            self.controller.handle_event(self, command)

        #self.exit_btn = Button(self.exit_Frame, text='Exit', padx=5, pady=5, command=lambda: send_event("EXIT"))
        self.myImg5 = PhotoImage(file='resources/BackButton.png')
        self.back_btn = Button(self.exit_Frame, image=self.myImg5, command=lambda: send_event("BACK"))
        #self.exit_btn.pack(side='right', fill="both", expand=True)
        self.back_btn.pack(side='right', fill="both", expand=True)

        # some title Frame --------------------------------------------------------------------->
        self.title_Frame = Frame(self.root)
        self.someTitle_lbl = Label(self.title_Frame, text='Classify Results', bg='#cbccd1')
        self.someTitle_lbl.config(font=("Courier", 34))
        self.someTitle_lbl.pack()

        # center table Frame ------------------------------------------------------------------->
        self.center_Frame = ttk.Notebook(self.root)


        # Matplotlib code Graph 1

        graph1 = Frame(self.center_Frame, bg='#cbccd1')

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, graph1)
        vectorizer.plot_dataframe(ax1)
        ax1.set_title('Labels')

        bar1.get_tk_widget().pack(side=TOP,fill=BOTH)

        self.center_Frame.add(graph1,text="Labels")


        # Bottom left menu
        self.returnMenu_Frame = Frame(self.root, pady=15, bg='#cbccd1')
        self.returnMenu_btn = Button(self.returnMenu_Frame, text='Export to Folders', padx=10,
                                     command=lambda: send_event("EXPORT_TO_FOLDERS"))
        self.saveCsv_btn = Button(self.returnMenu_Frame, text='Export CSV', padx=10,
                                  command=lambda: send_event("EXPORT_TO_CSV"))
        self.returnMenu_btn.pack(side=LEFT, padx=10)
        self.saveCsv_btn.pack(side=LEFT, padx=10)

        # self.saveCsv_Frame = Frame(self.root, pady=15, bg='#cbccd1')
        # self.saveCsv_btn = Button(self.saveCsv_Frame, text='Save to CSV')
        # self.saveCsv_btn.pack(side=RIGHT, padx=10)


        self.exit_Frame.grid(row=0, column=0, columnspan=2, sticky=E)
        self.title_Frame.grid(row=1, column=0, columnspan=2, pady=68, sticky=N + S)
        self.center_Frame.grid(row=2, column=0, columnspan=2, padx=65, sticky=N + S)
        self.returnMenu_Frame.grid(row=3, column=0, padx=65, sticky=W)

        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.mainloop()
