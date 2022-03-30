import pygame
import sys
from pygame.locals import *
from pygame import *
import tkinter
import pickle
import os
from tkinter.filedialog import asksaveasfile
import re #regular expression
from borderLineGenerator import BorderLineGenerator
from population import Population



class Tile: #Parent class
    __size = 10 #Pixel size of tile
    tileID = 0

    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.tileID = Tile.tileID
        Tile.tileID += 1

    def getSize():
        return Tile.__size
    
    def setSize(size):
        if Tile.__size is not None:
            Tile.__size = size

class Wall(Tile): #Child class which inherites the previous class' attributes and methods
    colour = (255,0,0) #sets clour to red
    def show(self, screen):
        #subroutine to display wall
        pygame.draw.rect(screen, Wall.colour, (self.x, self.y, Tile.getSize(), Tile.getSize())) #should draw the wall onto screen(the screen) using the colour
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, Tile.getSize(), Tile.getSize()),1)
         #updates pygame screen (not working for some reason)


class Track(Tile): #same thing but for the track (another type of tile so Tile is the parent class again
    colour = (0,255,255)
    def __init__(self, x, y):
        Tile.__init__(self, x, y)
        self.north = self.east = self.south = self.west = False

    def show(self, screen):
        pygame.draw.rect(screen, Track.colour, (self.x, self.y, Tile.getSize(), Tile.getSize()))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, Tile.getSize(), Tile.getSize()),1)
        pygame.display.update()


class statsBox:
    def __init__(self, x, y, w, h): #initialises class with x and y for positions and w and h for width/height
        self.x = x
        self.y = y
        self.w = w #width
        self.h = h #height

        pygame.font.init() #initialises font
        self.font = pygame.font.SysFont(None, 10) #sets font

    def show(self, screen, bestFitness, generationNum): 
        #subroutine to show the stats pane
        bestFitnessText = self.font.render("Best fitness: " + str(bestFitness), True, (0,0,0))
        generationNumtext = self.font.render("Current gen: " + str(generationNum), True, (0,0,0))

        pygame.draw.rect(screen, (220,220,220), (self.x, self.y, self.w, self.h))

        screen.blit(bestFitnessText, [self.x + 10, self.y + 10])
        screen.blit(generationNumtext, [self.x + 10, self.y + 50])
        pygame.display.update()
        

class Simulation:
    def __init__(self, MapDict, mutation, loadedWeights):
        pygame.init()
        SCREEN_W = pygame.display.Info().current_w
        SCREEN_H = pygame.display.Info().current_h


        (self.W, self.H) = self.setWindowSize(MapDict, (SCREEN_W - 100), (SCREEN_H - 100))

        self.screen = pygame.display.set_mode((self.W, self.H)) #initialises pygame display under variable screen
        self.screen.set_alpha(0) #alpha value determines transparency

        pygame.display.set_caption('grid') #caption for window
        self.fpsClock = pygame.time.Clock()
        self.screen.fill((0,255,0), rect = None) #screen col

        #info section
        pygame.draw.rect(self.screen, (220,220,220), (0, (self.H - Tile.getSize()), self.W, Tile.getSize())) #changed - to , (solved black screen error)
        self.statsPane = statsBox(0, (self.H - Tile.getSize()), self.W, Tile.getSize())
        


        (self.walls, self.tracks) = Simulation.generateMap(MapDict)

        for w in self.walls:
            w.show(self.screen)
        for t in self.tracks:
            t.show(self.screen)

        self.lines = BorderLineGenerator(self.tracks, MapDict["rows"], MapDict["columns"], Tile.getSize()).generate()

        self.CHECKPOINTS = self.calcCheckpoints()
        startTile = self.tracks[MapDict["startID"]]
        frontX = startTile.x + Tile.getSize()*1/3
        frontY = startTile.y + Tile.getSize()/2
        self.population = Population(30, (int(frontX), int(frontY)), int(Tile.getSize()*1/3), mutation)

        if loadedWeights is not None:
            self.population.cars[0].brain.weights1 = loadedWeights[0]
            self.population.cars[0].brain.weights2 = loadedWeights[1]
            self.population.cars[0].brain.weights3 = loadedWeights[2]
        
        self.animationLoop()
        

    def setWindowSize(self, MapDict, devW, devH):
        tileSize = 0
        while tileSize * ((MapDict["rows"] + 1)) < devH and tileSize * (MapDict["columns"]) < devW:
            tileSize += 1
        tileSize -= 1
        Tile.setSize(tileSize)
        return (tileSize * MapDict["columns"], tileSize * (MapDict["rows"] + 1))

    def calcCheckpoints(self):
        checkPoints = []
        size = Tile.getSize()

        for t in self.tracks:
            if t.north:
                northLine = ([(t.x, t.y), (t.x + size, t.y)])
                if northLine not in checkPoints:
                    checkPoints.append(northLine)
            if t.east:
                eastLine = ([(t.x + size, t.y), (t.x + size, t.y + size)])
                if eastLine not in checkPoints:
                    checkPoints.append(eastLine)
            if t.south:
                southLine = ([(t.x, t.y + size), (t.x + size, t.y + size)])
                if southLine not in checkPoints:
                    checkPoints.append(southLine)
            if t.west:
                westLine = ([(t.x, t.y), (t.x, t.y + size)])
                if westLine not in checkPoints:
                    checkPoints.append(westLine)

        return checkPoints


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
            for n in range(int(group[0])):
                if x > Tile.getSize()*(columns - 1):
                    x = 0
                    y += Tile.getSize()

                if group[1] == 'W':
                    walls.append(Wall(x,y))
                elif group[1] == 'T':
                    tracks.append(Track(x,y))

                x += Tile.getSize()
        return (walls, tracks)

    def saveWeights(self, weights):
        root = tkinter.Tk()
        root.withdraw

        file = asksaveasfile(initialdir= os.getcwd() + "\\weights", mode = 'wb', defaultextension=".pkl")

        if file is None:
            return pickle.dump(weights, file)

    def animationLoop(self):
        self.statsPane.show(self.screen, "", 1) #shows it's the first generation, no best fitness yet

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL: 
                    weights = [self.population.cars[-1].brain.weights1, self.population.cars[-1].brain.weights2, self.population.cars[-1].brain.weights3]
                    self.saveWeights(weights)

            if self.population.dead:
                self.population.createNextGeneration()
                self.statsPane.show(self.screen, self.population.bestCarFitness, self.population.generation) #updates stats pane

            for t in self.tracks:
                t.show(self.screen)

            self.population.update(self.lines, self.CHECKPOINTS)
            self.population.show(self.screen)

            for c in self.population.cars:
                if c.framesAlive >= 120 and len(c.collidedCheckPoints) == 0:
                    c.dead = True

            pygame.display.update()
            self.fpsClock.tick(60)


    

