# coding=utf-8
try:
    # python 3
    import tkinter
except:
    # python 2
    import Tkinter as tkinter
try:
    # python 2
    import ttk
except:
    # python 3
    import tkinter.ttk as ttk


import core.algorithm
import core.dup_finder
from utils import LOG

# GUI config
GUI_INPUT_PATH_NUM = 1


class DupFinderWindow(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.path_fields = list()
        for i in range(GUI_INPUT_PATH_NUM):
            self.path_label = tkinter.Label(self)
            self.path_label["text"] = "Path {0}:".format(str(i))
            if i == 0:
                self.path_label["text"] += "(Required)"
            else:
                self.path_label["text"] += "(Optional)"
            self.path_label.grid(row=i, column=0)

        for i in range(GUI_INPUT_PATH_NUM):
            self.path_field = tkinter.Entry(self)
            self.path_field["width"] = 50
            self.path_field.grid(row=i, column=1, columnspan=6)
            self.path_fields.append(self.path_field)

        self.find_btn = ttk.Button(self)
        self.find_btn["text"] = "Find"
        self.find_btn["command"] = self.start_find
        self.find_btn.grid(row=GUI_INPUT_PATH_NUM + 1, column=6)

    def start_find(self):
        LOG.debug("start_find button click")
        # do some input check

        # start to find
        filters = [
            core.algorithm.SizeFilter(),
            core.algorithm.CharacterFilter()
        ]
        paths = [path_field.get() for path_field in self.path_fields]
        LOG.debug(paths)
        dup_finder = core.dup_finder.DupFinder(paths, filters)
        dup_finder.find()
        dup_finder.dump2file("output.txt")
        dup_finder.dump2csv("output.csv")
