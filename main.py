#Program source code by Cathline Sean Dougan
#Project start 23/07/21
#Project end TBA
#Autonomous car simulation using neural networks and pygame

import sys
import os #to find files
import tkinter as tk #for display
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
import pickle #to save and load map
from typing import Type #for saving map
import MapDesign
import simulation as sim
import threading #Trying to solve tkinter 'Not Responding' problem


#Early August update: 03/08/2021
#Design menu created. Imports imported.
#Quit function completed
#Map Design function started
EMPTY_STRING = '' #Defined here just to make it easier

class Application(tk.Frame): #Self created class, a child class of tk.Frame which is imported from Tkinter
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.MapDict = None
        self.loadedWeights = None
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        self.displayMenu()
        global EMPTY_STRING
        



    def displayMenu(self): #Simple tkinter GUI creation
        menuTitle = tk.Label(self, text = "Welcome to Sean's Autonomous Car Simulation",
            foreground = "black",
            background = "white",
            font = self.fontStyle
        ).pack(side = 'top')
        self.designMap = tk.Button(self, text = 'DESIGN A MAP', font = self.fontStyle, bg = 'black', fg = 'white', command = self.getMapinfo).pack(side = 'top')
        self.runSimulation = tk.Button(self, text = 'RUN SIMULATION', font = self.fontStyle, bg = 'black', fg = 'white', command = self.getSiminfo).pack(side = 'top')
        self.obstacles = tk.Button(self, text = 'ADD/REMOVE OBSTACLES', font = self.fontStyle, bg = 'black', fg = 'white', command = self.getObstacles).pack(side = 'top')
        self.quit = tk.Button(self, text = 'QUIT', font = self.fontStyle, bg = 'black', fg = 'white', command = self.master.destroy).pack(side = 'bottom')

    def getMapinfo(self): #Attribute used to create a new tkinter window to ask for Map dimensions
        sizeWindow = tk.Tk()
        sizeWindow.title("Grid dimensions")

        rowMessage = tk.Label(sizeWindow, text = 'Enter the number of rows')
        self.rowInput = tk.Entry(sizeWindow, bd = 5)
        columnMessage = tk.Label(sizeWindow, text = 'Enter the number of columns')
        self.columnInput = tk.Entry(sizeWindow, bd = 5)
        allez = tk.Button(sizeWindow, text = 'START', bg = 'green', command = self.createMap)

        rowMessage.grid(row = 0, column = 0)
        self.rowInput.grid(row = 0, column = 1)
        columnMessage.grid(row = 1, column = 0)
        self.columnInput.grid(row = 1, column = 1)
        allez.grid(row = 2, column = 1)

        sizeWindow.mainloop()




    def createMap(self):

        root = tk.Tk()
        try: #Exception handling
            MapDesign.MapCreation(int(self.rowInput.get()),int(self.columnInput.get()), master = root) #Grabs values and creates a window
        except ValueError: #If the value entered is not an integer or no value has been entered this part of the program will run
            root.withdraw()
            messagebox.showinfo("Entry error", "Please retry entering values") #messagebox shows message for error
        

    def getSiminfo(self):
        menuWindow = tk.Tk()
        showMutation  = tk.Label(menuWindow, text = 'mutation level = ').pack(side = 'left')
        self.mutationEntry = tk.Entry(menuWindow, bd = 5)
        self.mutationEntry.pack(side = 'left')

        selectMap = tk.Button(menuWindow, text = 'SELECT MAP', font = self.fontStyle, bg = 'black', fg = 'white', command = self.getMapfile).pack(side = 'bottom')
        selectWeights = tk.Button(menuWindow, text = 'SELECT WEIGHTS FILE', font = self.fontStyle, bg = 'black', fg = 'white', command = self.loadWeights).pack(side = 'bottom')


        startButton = tk.Button(menuWindow, text = 'START', command = self.runSim).pack(side = 'bottom')



    def getObstacles(self):
        pass

    def runSim(self):
        mutation = self.mutationEntry.get()
        if self.MapDict == None:
            messagebox.showinfo("Map not selected","Please select a map before continuing!")
        else:
            try:
                if mutation == "":
                    raise TypeError

                else:
                    mutation = int(mutation)
                    if 0 > mutation or 100 < mutation:
                        raise ValueError
                    else:
                        newSimulation = sim.Simulation(self.MapDict, mutation, self.loadedWeights) #Instantiates Simulation (concrete class) for it to be run
            except ValueError: #Separate exception handling code depending on the error
                messagebox.showinfo("ValueError", "Mutation entry must be an integer")
                self.mutationEntry.delete(0,len(self.mutationEntry.get())) #Clears entry box
            except TypeError:
                mutation = 30
                #messagebox.showinfo("","Invalid mutation level, Enter again")


    def loadWeights(self): #Opens weights file
        file = askopenfilename(initialdir= os.getcwd() + "\\weights", filetypes=(("PKL File", "*.pkl"),("All Files", "*.*")), title = "Choose file")
        try: 
            with open(file, 'rb') as pkl_file:
                self.loadWeights = pickle.load(pkl_file)
        except:
            messagebox.showinfo("", "File not retrieved, try again")


    def getMapfile(self): #Opens map file
        file = askopenfilename(filetypes=(("PKL Files", "*.pkl"),))
        try:
            with open(file, 'rb') as pkl_file:
                self.MapDict = pickle.load(pkl_file)
        except:
            messagebox.showinfo("Error", "File not found, try again")



if __name__ == "__main__":
    cwd = os.getcwd()
    try: 
        os.makedirs(cwd + '/weights') #makes a weights folder
    except:
        pass

    try:
        os.makedirs(cwd + '/maps') #makes a map folder
    except:
        pass


    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()







