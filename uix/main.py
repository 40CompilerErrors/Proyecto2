from tkinter import *

from proyecto_1.uix import MainScreen as MS


class MainApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Bienvenidos")
        self.geometry('950x850')
        self.minsize(950, 850)
        self.config(bd='10')
        self.config(relief='groove')
        # self.config(bg='#cbccd1')

        # the container is where we'll stack a bunch of frames
        self.container = Container(self)
        self.container.config(bg='#cbccd1')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        MS.MainScreen(self.container)


class Container(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.frame_stack = {}

    def remove_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def previous_frame(self):
        # TODO
        pass


if __name__ == "__main__":
    # execute only if run as a script
    MainApp()
