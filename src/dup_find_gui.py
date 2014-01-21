try:
    import tkinter
except:
    import Tkinter as tkinter

import gui.main


if __name__ == '__main__':
    root = tkinter.Tk()
    app = gui.main.DupFinderWindow(master=root)
    app.mainloop()
