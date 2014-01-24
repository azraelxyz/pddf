# coding=utf-8
try:
    # python 3
    import tkinter
    from tkinter import filedialog
    from tkinter import messagebox as messagebox
except ImportError:
    # python 2
    import tkFileDialog as filedialog
    import Tkinter as tkinter
    import tkMessageBox as messagebox

try:
    # python 2
    import ttk
except ImportError:
    # python 3
    import tkinter.ttk as ttk

import os

import core.algorithm
import core.dup_finder
from utils import LOG

#GUI_INPUT_PATH_NUM = 1

INITIAL_DIR = os.getcwd()


class DupFinderWindow(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.path_label = tkinter.Label(self)
        self.path_label["text"] = "Path(Required):"
        self.path_label.grid(row=0, column=0)

        self.path_field = tkinter.Label(self)
        self.path_field["width"] = 50
        self.path_field["text"] = INITIAL_DIR
        self.path_field.grid(row=0, column=1, columnspan=6)

        self.dir_btn = ttk.Button(self)
        self.dir_btn["text"] = "Open"
        self.dir_btn["command"] = self.open_dir
        self.dir_btn.grid(row=0, column=7)

        self.find_btn = ttk.Button(self)
        self.find_btn["text"] = "Find"
        self.find_btn["command"] = self.start_find
        self.find_btn.grid(row=1, column=7)

    def open_dir(self):
        path = filedialog.askdirectory(initialdir=INITIAL_DIR)
        self.path_field.config(text=path)

    def start_find(self):
        LOG.debug("start_find button click")
        LOG.debug(self.path_field.cget("text"))
        # do some input check
        # start to find
        filters = [
            core.algorithm.SizeFilter(),
            core.algorithm.CharacterFilter()
        ]
        paths = [self.path_field.cget("text")]
        LOG.debug(paths)
        dup_finder = core.dup_finder.DupFinder(paths, filters)
        dup_finder.find()
        dup_finder.dump2file("output.txt")
        dup_finder.dump2csv("output.csv")
        messagebox.showinfo('', 'find complete')
