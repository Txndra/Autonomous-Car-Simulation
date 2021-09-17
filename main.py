#Program source code by Cathline Sean Dougan
#Project start 23/07/21
#Project end TBA
#Autonomous car simulation using neural networks and pygame

import sys
import os

import pygame
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
import pickle
import MapDesign
from car import run_simulation


#Early August update: 03/08/2021
#Design menu created. Imports imported.
#Quit function completed
#Map Design function started


class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.Weights = None
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        self.displayMenu()
        



    def displayMenu(self):
        menuTitle = tk.Label(self, text = "Welcome to Sean's Autonomous Car Simulation",
            foreground = "black",
            background = "white",
            font = self.fontStyle
        ).pack(side = 'top')
        self.designMap = tk.Button(self, text = 'DESIGN A MAP', font = self.fontStyle, bg = 'black', fg = 'white', command = self.getMapinfo).pack(side = 'top')
        self.runSimulation = tk.Button(self, text = 'RUN SIMULATION', font = self.fontStyle, bg = 'black', fg = 'white', command = runSim).pack(side = 'top')
        self.obstacles = tk.Button(self, text = 'ADD/REMOVE OBSTACLES', font = self.fontStyle, bg = 'black', fg = 'white', command = self.getObstacles).pack(side = 'top')
        self.quit = tk.Button(self, text = 'QUIT', font = self.fontStyle, bg = 'black', fg = 'white', command = self.master.destroy).pack(side = 'bottom')

    def getMapinfo(self):
        sizeWindow = tk.Tk()
        sizeWindow.title("Grid dimensions")

        rowMessage = tk.Label(sizeWindow, text = 'Enter the number of rows')
        self.rowInput = tk.Entry(sizeWindow, bd = 5)
        columnMessage = tk.Label(sizeWindow, text = 'Enter the number of columns')
        self.columnInput = tk.Entry(sizeWindow, bd = 5)
        allez = tk.Button(sizeWindow, text = 'START', bg = 'green', command = self.createMap)

        rowMessage.grid(row = 0, column = 0)
        self.rowInput.grid(row = 0, column = 1) #ctrl C
        columnMessage.grid(row = 1, column = 0)
        self.columnInput.grid(row = 1, column = 1)
        allez.grid(row = 2, column = 1)

        sizeWindow.mainloop()


    def createMap(self):
        root = tk.Tk()
        try:
            MapDesign.MapCreation(int(self.rowInput.get()),int(self.columnInput.get()), master = root) #Grabs values and creates a window
        except ValueError:
            root.withdraw() #Doesn't show the window
            messagebox.showinfo("Entry error", "Please retry entering values") #messagebox shows message for error


    def getSiminfo(self):
        pass
        

    def getObstacles(self):
        pass

    

def runSim():
        exec(open(r"C:\Users\sdgam\OneDrive\Documents\AUTONOMOUS CARSIM\A-Level-NEA---Autonomous-Car\A-Level-NEA---Autonomous-Car\car.py").read())

    




root = tk.Tk()
app = Application(master = root)
app.mainloop()





