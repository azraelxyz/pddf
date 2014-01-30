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
import threading
import time

import core.algorithm
import core.dup_finder
from utils import LOG

INITIAL_DIR = os.getcwd()


class DupFinderWindow(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.find_thread = None
        self.status_thread = None
        self.find_complete = False

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

        # status field
        self.status_field = tkinter.Label(self, text="")
        self.status_field.grid(row=4, column=0, columnspan=7)

        # full scan checkbutton
        self.full_scan = tkinter.BooleanVar()
        self.full_scan_chk = tkinter.Checkbutton(self, text="Full Scan",
                                                 variable=self.full_scan)
        self.full_scan_chk.grid(row=5, column=0)

        # csv
        self.output_csv = tkinter.BooleanVar()
        self.output_csv_chk = tkinter.Checkbutton(self, text="Output a CSV",
                                                 variable=self.output_csv)
        self.output_csv_chk.grid(row=5, column=2)

        # find button
        self.find_btn = ttk.Button(self)
        self.find_btn["text"] = "Find"
        self.find_btn["command"] = self.start_find
        self.find_btn.grid(row=5, column=7)

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

    def disable_all(self):
        self.find_btn.configure(state=tkinter.DISABLED)
        self.dir_btn1.configure(state=tkinter.DISABLED)
        self.dir_btn2.configure(state=tkinter.DISABLED)
        self.dir_btn3.configure(state=tkinter.DISABLED)
        self.dir_btn4.configure(state=tkinter.DISABLED)
        self.output_csv_chk.configure(state=tkinter.DISABLED)
        self.full_scan_chk.configure(state=tkinter.DISABLED)

    def enable_all(self):
        self.find_btn.configure(state=tkinter.NORMAL)
        self.dir_btn1.configure(state=tkinter.NORMAL)
        self.dir_btn2.configure(state=tkinter.NORMAL)
        self.dir_btn3.configure(state=tkinter.NORMAL)
        self.dir_btn4.configure(state=tkinter.NORMAL)
        self.output_csv_chk.configure(state=tkinter.NORMAL)
        self.full_scan_chk.configure(state=tkinter.NORMAL)

    def start_find(self):
        LOG.debug("start_find button click")
        self.disable_all()
        # start to find
        paths = [self.path_field1.get()]
        if (self.path_field2.get()):
            paths.append(self.path_field2.get())
        if (self.path_field3.get()):
            paths.append(self.path_field3.get())
        if (self.path_field4.get()):
            paths.append(self.path_field4.get())
        LOG.debug(paths)
        LOG.debug("Full Scan {0}".format(str(self.full_scan.get())))
        LOG.debug("Ouput csv {0}".format(str(self.output_csv.get())))
        do_it = messagebox.askyesno('',
                    'It may take several minutes to complete please wait')
        if not do_it:
            self.enable_all()
            return
        self.find_complete = False
        filters = [
            core.algorithm.SizeFilter(),
            core.algorithm.CharacterFilter()
        ]
        if (self.full_scan.get()):
            filters.append(core.algorithm.FullScanner())
        dup_finder = core.dup_finder.DupFinder(paths, filters)
        self.status_thread = threading.Thread(target=self.update_status,
                                                    args=(dup_finder,))
        self.find_thread = threading.Thread(target=self.background_find,
                                                    args=(dup_finder,))
        self.find_thread.start()
        self.status_thread.start()

    def update_status(self, dup_finder):
        while True:
            time.sleep(2)
            step = dup_finder.get_step()
            count = dup_finder.get_progress()
            total = dup_finder.get_total()
            if total:
                status = "{0}: {1}/{2}".format(step, str(count), str(total))
            else:
                status = "{0}: {1}".format(step, str(count))
            self.status_field.config(text=status)
            if self.find_complete == True:
                self.status_field.config(text="Find complete!!")
                break

    def background_find(self, dup_finder):
        dup_finder.find()
        if (self.output_csv.get()):
            output_file = os.path.join(os.getcwd(), "output.csv")
            dup_finder.dump2csv(output_file)
        else:
            output_file = os.path.join(os.getcwd(), "output.txt")
            dup_finder.dump2file(output_file)
        self.find_complete = True
        messagebox.showinfo('',
                'find complete, please check {0}'.format(output_file))
        self.enable_all()
