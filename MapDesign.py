import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import pickle
import os
from Stack import Stack 




class userButtons:
    trackColour = (51,255,51)
    wallColour = (255,0,0)
    buttonCount = 0
    startup = False
    currentStack = None

    def __init__(self, r, c, win):
        self.Button = tk.Button(win, bg = userButtons.fromRGB(userButtons.wallColour), command = self.changeColour, width = 6, height = 3)
        self.Button.grid(row=r,column=c)
        self.buttonType = 'W'
        self.id = userButtons.buttonCount
        userButtons.buttonCount += 1

    def changeColour(self):
        userButtons.currentStack.push([self.buttonType + str(self.id)]) #This pushes the info onto the stack (LiFo)
        if userButtons.startup:
            self.pickStart()
            userButtons.startup = False
        else:
            if self.buttonType == 'W':
                self.makeTrack()
            elif self.buttonType == 'T' or self.buttonType == 'S':
                self.makeWall()

    def makeTrack(self):
        self.buttonType = 'T'
        self.Button.config(text='', bg=userButtons.fromRGB(userButtons.trackColour))
    def pickStart(self):
        self.buttonType = 'S'
        self.Button.config(text="S", bg=userButtons.fromRGB(userButtons.trackColour))
    def makeWall(self):
        self.buttonType = 'W'
        self.Button.config(text="", bg=userButtons.fromRGB(userButtons.wallColour))  
    
    def fromRGB(rgb):
        return "#%02x%02x%02x" % rgb

class MapCreation(tk.Frame):
    def __init__(self, rows, columns, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("MAP CREATOR")
        self.pack()
        self.buttons = []
        self.rows = rows
        self.columns = columns
        self.createWidgets()

    def createWidgets(self):
        mapFrame = tk.Frame(self.master)
        mapFrame.pack(side = 'top')
        #Frame for the whole map

        optionsFrame = tk.Frame(self.master)
        optionsFrame.pack(side = 'bottom')
        #Creates a frame ready for options to be added

        userButtons.currentStack = Stack(15)
        for r in range(self.rows):
            for c in range(self.columns):
                self.buttons.append(userButtons(r,c,mapFrame))

        #creates the map creator in the correct size

        startButton = tk.Button(optionsFrame, text = 'PICK START TILE', command = self.startButton).grid(row = 0, column = 0)
        undoButton = tk.Button(optionsFrame, text = 'UNDO', command = self.undo).grid(row = 0, column = 1)
        clearButton = tk.Button(optionsFrame, text = 'CLEAR ALL', command = self.clearMap).grid(row = 1 , column = 0)
        saveButton = tk.Button(optionsFrame, text = 'SAVE', command = self.saveMap).grid(row = 1 , column = 0)

        #Some options for creating the map
        
    def startButton(self):
        buttonDeya = False
        for i in self.buttons:
            if i.buttonType == 'S':
                messagebox.showinfo("","Try removing the current start button before adding a new one")
                buttonDeya = True
        if not buttonDeya:
            messagebox.showinfo("","Click on a tile to make it the new starting tile")
            userButtons.startup = True

    def undo(self):
        returnVal = userButtons.currentStack.pop()
        for x in returnVal:
            tileType = x[0] #This will return the button type
            tileID = x[1:] #This shows the ID

            if tileType == 'W':
                self.buttons[tileID].makeWall()
            elif tileType == 'T':
                self.buttons[tileID].makeTrack()
            elif tileType == 'W':
                self.buttons[tileID].pickStart()

    def clearMap(self):
        pass

    def saveMap(self):
        pass
















        