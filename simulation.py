import pygame
import sys
from pygame.locals import *
import tkinter
import pickle
import os
from tkinter.filedialog import asksaveasfile
import re #regular expression
from borderLineGenerator import BorderLineGenerator

class Tile:
    __size = 10
    tileID = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tileID = Tile.tileID
        Tile.tileID += 1

    def getSize():
        return Tile.__size
    
    def setSize(size):
        if Tile.__size is not None:
            Tile.__size = size

class Wall(Tile):
    colour = (255,0,0)
    def show(self, SCR):
        pygame.draw.rect(SCR, Wall.colour, (self.x, self.y, Tile.getSize(), Tile.getSize()))
        pygame.draw.rect(SCR, (255, 255, 255), (self.x, self.y, Tile.getSize(), Tile.getSize()),1)


class Track(Tile):
    colour = (0,255,255)
    def show(self, SCR):
        pygame.draw.rect(SCR, Wall.colour, (self.x, self.y, Tile.getSize(), Tile.getSize()))
        pygame.draw.rect(SCR, (255, 255, 255), (self.x, self.y, Tile.getSize(), Tile.getSize()),1)


class statsBox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w #width
        self.h = h #height

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 10)

    def show(self, SCR, bestFitness, generationNum):
        bestFitnessText = self.font.render("Best fitness: ", + str(bestFitness), False, (0,0,0))
        generationNumtext = self.font.render("Current gen: " + str(generationNum), False, (0,0,0))

        pygame.draw.rect(SCR, (220,220,220), (self.x, self.y, self.w, self.h))

        SCR.blit(bestFitnessText, (self.x + 10, self.y + 10))
        SCR.blit(generationNumtext, (self.x + 10, self.y + 50))

class Simulation:
    def __init__(self, MapDict, mutation, loadedWeights):
        pygame.init()

        SCREEN_W = pygame.display.Info().current_w
        SCREEN_H = pygame.display.Info().current_h


        (self.W, self.H) = self.setWindowSize(MapDict, (SCREEN_W - 100), (SCREEN_H - 100))

        self.SCR = pygame.display.set_mode((self.W, self.H))
        self.SCR.set_alpha(0)

        pygame.display.set_caption('grid') #caption for window
        self.fpsClock = pygame.time.Clock()
        self.SCR.fill((0,255,0), rect = None) #screen col

        #info section
        pygame.draw.rect(self.SCR, (220,220,220), (0, (self.H - Tile.getSize()), self.W - Tile.getSize()))
        self.statsPane = statsBox(0, (self.H - Tile.getSize()), self.W - Tile.getSize())


        (self.walls, self.tracks) = Simulation.generateMap(MapDict)

        for w in self.walls:
            w.show(self.SCR)
        for t in self.tracks:
            t.show(self.SCR)


        startTile = self.tracks[MapDict["startID"]]

    def generateMap(MapDict):
        rows = MapDict["rows"]
        columns = MapDict["columns"]
        mapRLE = MapDict["data"]

        mapRLEarray = re.split(r'(\d+)', mapRLE)[1:]
        mapRLE2Darray = []
        for i in range(0, len(mapRLEarray), 2):
            mapRLE2Darray.append([mapRLEarray[i], mapRLEarray[i+1]])


        #create tiles
        walls = []
        tracks = []
        x = 0
        y = 0
        for group in mapRLE2Darray: 
            for e in range(int(group[0])):
                if x > Tile.getsize()*(columns - 1):
                    x = 0
                    y += Tile.getsize()

                if group[1] == 'W':
                    walls.append(Wall(x,y))
                elif group[1] == 'T':
                    tracks.append(Track(x,y))

                x += Tile.getsize()
        return (walls, tracks)

    

