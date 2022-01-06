from numpy.lib.function_base import angle
from neural import Neural
import pygame
from pygame.math import Vector2
from radar import radars

class Car:
    beamAngles = [-45, 0, 45] #angles for the car beams
    __SIZE = None
    beamCarOffset = 10
    idCounter = 0
    
    def __init__(self, frontP):
        self.id = Car.idCounter
        Car.idCounter += 1

        self.brain = Neural() # Instantiates neural network to car
        self.framesAlive = 0
        self.fitness = 0
        self.dead = False #Boolean to check whether car is dead

        self.bestOfPrevGen = False #Will be True if car selected has the highest fitness
        self.collidedCheckPoints = []
        #self.sprite = pygame.image.load(r"car.png").convert()
        self.vel = Vector2(1,0)
        self.nextPoint = frontP + self.vel

        self.frontPoint = self.nextPoint#make front of triangle/car
        self.leftPoint = self.frontPoint + Vector2(-Car.__SIZE,0).rotate(30)
        self.rightPoint = self.frontPoint + Vector2(-Car.__SIZE,0).rotate(-30)
        self.angle = 0  

        #create beams
        self.beams = []
        for a in Car.beamAngles:
            beamOrigin = self.frontPoint - Vector2(Car.beamCarOffset, 0).rotate(self.angle)
            self.beams.append(radars(beamOrigin, a))
        self.edges = []

    def update(self, borderLines):
        self.framesAlive += 1

        brainInput = [b.length/50 for b in self.beams]
        brainInput.append(self.vel.length() / (Car.__SIZE/2))

        (angleChange, acceleration) = self.brain.calculateOutput(brainInput) #Uses FF Neural Network to calculate the change in angle and acceleration
        acceleration += 0.5

        if (Vector2(self.vel)).length() >= Car.__SIZE/2 and acceleration > 1:
            acceleration = 0

        self.frontPoint = self.nextPoint

        if angleChange > 0:
            self.angle = (self.angle + angleChange) % 360 #Mods with 360 so the answer is between  0 and 360
        else:
            self.angle = (self.angle + angleChange) % -360

        self.leftPoint = self.frontPoint + Vector2(-Car.__SIZE, 0).rotate(30 + self.angle)
        self.rightPoint = self.frontPoint + Vector2(-Car.__SIZE, 0).rotate(-30 + self.angle)

        self.nextPoint = self.frontPoint + Vector2(self.vel * acceleration).rotate(self.angle)

        self.edges = [[self.leftPoint, self.frontPoint], [self.frontPoint, self.rightPoint], [self.rightPoint, self.leftPoint]]

        for b in self.beams:
            beamOrigin = self.frontPoint - Vector2(Car.beamCarOffset, 0).rotate(self.angle)

            b.update(beamOrigin, angleChange, borderLines)

    #draws car
    def show(self, SCR):
        carCol = (221, 160, 221)
        if self.bestOfPrevGen:
            carCol = (120, 80, 34)

        pygame.draw.polygon(SCR, carCol, (self.leftPoint, self.frontPoint, self.rightPoint))
        pygame.draw.circle(SCR, (255,255,255), (int(self.frontPoint[0]), int(self.frontPoint[1])), 2)
        pygame.draw.aaline(SCR, (0, 0, 100), self.frontPoint, self.nextPoint, 1)

        for b in self.beams:
            b.show(SCR)

    def getSize():
        return Car.__SIZE
    def setSize(size):
        Car.__SIZE = size
        







