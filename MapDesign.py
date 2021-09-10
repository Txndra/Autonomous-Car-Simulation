import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pickle



class Map:
    def __init__(self):
        self.mapSize = []
        
    

    def getSize(self):
        messageBox = tk.Tk()
        sizeMessage = tk.Label(
        text = "ENTER MAP SIZE",
        )
        getWidth = tk.Entry(messageBox)
        sizeMessage.pack()
        getWidth.pack()
        messageBox.mainloop()





        