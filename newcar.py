from numpy.lib.function_base import angle
from neural import Neural
import pygame
from pygame.math import Vector2
from radar import radars
import math

class Car:
    #static class variables here
    beamAngles = [-45, 0, 45] #angles for the car beams
    __SIZE = None
    beamCarOffset = 10
    idCounter = 0
    
    def __init__(self, frontPoint):
        self.id = Car.idCounter
        Car.idCounter += 1
        self.sprite = pygame.image.load(r"car.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (Car.__SIZE, Car.__SIZE))
        self.sprite.set_colorkey(0,255,120)
        self.rotatedsprite = self.sprite
        self.center = [frontPoint[0] + Car.__SIZE/2, frontPoint[1] + Car.__SIZE/2]
        self.brain = Neural() # Instantiates neural network to car
        self.framesAlive = 0
        self.fitness = 0
        self.dead = False#Boolean to check whether car is dead

        self.bestOfPrevGen = False #Will be True if car selected has the highest fitness
        self.collidedCheckPoints = []
        #self.sprite = pygame.image.load(r"car.png").convert() 
        self.angle = 0  
        self.vel = Vector2(1,0)
        self.nextPoint = frontPoint + self.vel
        self.frontPoint = self.nextPoint
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
        acceleration += 1

        if (Vector2(self.vel)).length() >= Car.__SIZE/2 and acceleration > 1:
            acceleration = 0

        self.frontPoint = self.nextPoint

        if angleChange > 0:
            self.angle = (self.angle + angleChange) % 360 #Mods with 360 so the answer is between  0 and 360
        else:
            self.angle = (self.angle + angleChange) % -360

        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        length = 0.5 * Car.__SIZE
        self.nextPoint = self.frontPoint + Vector2(self.vel * acceleration).rotate(self.angle)
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * (0.5* Car.__SIZE)]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * (0.5* Car.__SIZE)]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * (0.5* Car.__SIZE)]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * (0.5* Car.__SIZE)]

        self.edges = [left_top, right_top, left_bottom, right_bottom]

        for b in self.beams:
            beamOrigin = self.frontPoint - Vector2(Car.beamCarOffset, 0).rotate(self.angle)

            b.update(beamOrigin, angleChange, borderLines)

    #draws car
    def show(self, screen):
        screen.blit(self.rotated_sprite, self.frontPoint)
        #pygame.draw.polygon(screen, carCol, (self.frontPoint, ((self.rightPoint+self.leftPoint)/2)), 15)

        pygame.draw.circle(screen, (255,255,255), (int(self.frontPoint[0]), int(self.frontPoint[1])), 2)
        pygame.draw.aaline(screen, (0, 0, 100), self.frontPoint, self.nextPoint, 1)

        for b in self.beams:
            b.show(screen)

    def rotate_center(self, image, Theangle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, Theangle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def getSize():
        return Car.__SIZE
        
    def setSize(size):
        Car.__SIZE = size
