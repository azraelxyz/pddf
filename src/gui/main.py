# coding=utf-8
try:
    import tkinter
except:
    import Tkinter as tkinter

import setting


class DupFinderWindow(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        for i in range(setting.GUI_INPUT_PATH_NUM):
            self.path_label = tkinter.Label(self)
            self.path_label["text"] = "Path {0}:".format(str(i))
            self.path_label.grid(row=i, column=0)
            self.path_field = tkinter.Entry(self)
            self.path_field["width"] = 50
            self.path_field.grid(row=i, column=1, columnspan=6)

        self.new = tkinter.Button(self)
        self.new["text"] = "New"
        self.new.grid(row=setting.GUI_INPUT_PATH_NUM + 1, column=6)
