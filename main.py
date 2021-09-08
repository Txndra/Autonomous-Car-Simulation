#Program source code by Cathline Sean Dougan
#Project start 23/07/21
#Project end TBA
#Autonomous car simulation using neural networks and pygame
import math
import numpy
import random
import sys
import os

import pygame

import tkinter as tk
import tkinter.font as tkFont

#Early August update: 03/08/2021
#Design menu created. Imports imported.
#Quit function completed
#Map Design function started

def MapDesign():
    directory = "C:\WINDOWS\system32\mspaint.exe"
    os.startfile(directory)
    #os.system(directory)
    message = tk.Label(
        text = "When you have made your map, save it in the file 'AUTONOMOUS CARSIM'"
        )   
    message.pack()
    

def Simulation():
    directory = r"C:\Users\sdgam\OneDrive\Documents\AUTONOMOUS CARSIM\A-Level-NEA---Autonomous-Car\car.py"
    os.startfile(directory)
    

def com3():
    pass

def displayMenu():
    window = tk.Tk()
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    title = tk.Label(
        text = "Welcome to Sean's Autonomous Car Simulation",
        foreground = "black",
        background = "white",
        font = fontStyle
    )

    title.pack()
    
    #Map Design option
    
    askMapDesign = tk.Button(
        text = "DESIGN A MAP",
        width = 80,
        height = 5,
        bg = "black",
        fg = "white", command = MapDesign
        
    )

    askMapDesign.pack()

    #Add Obstacles option

    askObstacles = tk.Button(
        text = "ADD/REMOVE OBSTACLES",
        width = 80,
        height = 5,
        bg = "black",
        fg = "white",
    )

    askObstacles.pack()
                             

    #Run Simulation option

    askRunSim = tk.Button(
        text = "RUN SIMULATION",
        width = 80,
        height = 5,
        bg = "black",
        fg = "white", command = Simulation
        
    )

    askRunSim.pack()

    #Quit option
    
    askQuit = tk.Button(
        text = "QUIT",
        width = 80,
        height = 5,
        bg = "black",
        fg = "white", command=quit
       
    )
    
    askQuit.pack()
    
    window.mainloop()

displayMenu()


