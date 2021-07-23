#Program source code by Cathline Sean Dougan
#Project start 23/07/21
#Project end TBA
#Autonomous car simulation using neural networks and pygame
import pygame as py
import sys
import random
import tkinter as tk
import tkinter.font as tkFont
import numpy

def com1():
    pass

def com2():
    pass

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
    
    askMapDesign = tk.Button(
        text="Design a map",
        width=25,
        height=5,
        bg="black",
        fg="white",
        
    )

    askMapDesign.pack()
    
    askRunSim = tk.Button(
        text="Run simulation",
        width=25,
        height=5,
        bg="black",
        fg="white",
        
    )

    askRunSim.pack()
    
    askViewStats = tk.Button(
        text="View stats",
        width=25,
        height=5,
        bg="black",
        fg="white",
        
    )
    
    askViewStats.pack()
    
    askQuit = tk.Button(
        text="Quit",
        width=25,
        height=5,
        bg="black",
        fg="white", command=quit
       
    )
    
    askQuit.pack()
    
    window.mainloop()

displayMenu()


