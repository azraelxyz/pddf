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
        # path field 1
        self.path_label1 = tkinter.Label(self)
        self.path_label1["text"] = "Path 1 (Required):"
        self.path_label1.grid(row=0, column=0)

        self.path1 = tkinter.StringVar()
        self.path_field1 = tkinter.Entry(self,
                                        state="readonly",
                                        textvariable=self.path1,
                                        width=50)
        self.path1.set(INITIAL_DIR)
        self.path_field1.grid(row=0, column=1, columnspan=6)

        self.dir_btn1 = ttk.Button(self)
        self.dir_btn1["text"] = "Open"
        self.dir_btn1["command"] = self.open_dir1
        self.dir_btn1.grid(row=0, column=7)

        # path field 2
        self.path_label2 = tkinter.Label(self)
        self.path_label2["text"] = "Path 2 (Optional):"
        self.path_label2.grid(row=1, column=0)

        self.path2 = tkinter.StringVar()
        self.path_field2 = tkinter.Entry(self,
                                        state="readonly",
                                        textvariable=self.path2,
                                        width=50)
        self.path2.set("")
        self.path_field2.grid(row=1, column=1, columnspan=6)

        self.dir_btn2 = ttk.Button(self)
        self.dir_btn2["text"] = "Open"
        self.dir_btn2["command"] = self.open_dir2
        self.dir_btn2.grid(row=1, column=7)

        # path field 3
        self.path_label3 = tkinter.Label(self)
        self.path_label3["text"] = "Path 3 (Optional):"
        self.path_label3.grid(row=2, column=0)

        self.path3 = tkinter.StringVar()
        self.path_field3 = tkinter.Entry(self,
                                        state="readonly",
                                        textvariable=self.path3,
                                        width=50)
        self.path3.set("")
        self.path_field3.grid(row=2, column=1, columnspan=6)

        self.dir_btn3 = ttk.Button(self)
        self.dir_btn3["text"] = "Open"
        self.dir_btn3["command"] = self.open_dir3
        self.dir_btn3.grid(row=2, column=7)

        # path field 4
        self.path_label4 = tkinter.Label(self)
        self.path_label4["text"] = "Path 4 (Optional):"
        self.path_label4.grid(row=3, column=0)

        self.path4 = tkinter.StringVar()
        self.path_field4 = tkinter.Entry(self,
                                        state="readonly",
                                        textvariable=self.path4,
                                        width=50)
        self.path4.set("")
        self.path_field4.grid(row=3, column=1, columnspan=6)

        self.dir_btn4 = ttk.Button(self)
        self.dir_btn4["text"] = "Open"
        self.dir_btn4["command"] = self.open_dir4
        self.dir_btn4.grid(row=3, column=7)

        # find button
        self.find_btn = ttk.Button(self)
        self.find_btn["text"] = "Find"
        self.find_btn["command"] = self.start_find
        self.find_btn.grid(row=4, column=7)

    def open_dir1(self):
        path = filedialog.askdirectory(initialdir=self.path_field1.get())
        if path:
            self.path1.set(path)

    def open_dir2(self):
        init_dir = INITIAL_DIR
        if self.path_field2.get():
            init_dir = self.path_field2.get()
        path = filedialog.askdirectory(initialdir=init_dir)
        if path:
            self.path2.set(path)

    def open_dir3(self):
        init_dir = INITIAL_DIR
        if self.path_field3.get():
            init_dir = self.path_field3.get()
        path = filedialog.askdirectory(initialdir=init_dir)
        if path:
            self.path3.set(path)

    def open_dir4(self):
        init_dir = INITIAL_DIR
        if self.path_field4.get():
            init_dir = self.path_field4.get()
        path = filedialog.askdirectory(initialdir=init_dir)
        if path:
            self.path4.set(path)

    def start_find(self):
        LOG.debug("start_find button click")
        # start to find
        filters = [
            core.algorithm.SizeFilter(),
            core.algorithm.CharacterFilter()
        ]
        paths = [self.path_field1.get()]
        if (self.path_field2.get()):
            paths.append(self.path_field2.get())
        if (self.path_field3.get()):
            paths.append(self.path_field3.get())
        if (self.path_field4.get()):
            paths.append(self.path_field4.get())
        LOG.debug(paths)
        dup_finder = core.dup_finder.DupFinder(paths, filters)
        dup_finder.find()
        dup_finder.dump2file("output.txt")
        dup_finder.dump2csv("output.csv")
        messagebox.showinfo('', 'find complete')
