import math
import random
import sys
import os

import neat
import pygame
from pygame.locals import *


WIDTH = 1920
HEIGHT = 1080

carWidth = 60
carHeight = 60 

white = (255,255,255,255) #If car touches this colour it will crash
green = (0,255,0) #For drawing radars

generation = 0

class Car:
    def __init__(self):
        self.sprite = pygame.image.load(r"C:\Users\sdgam\OneDrive\Documents\AUTONOMOUS CARSIM\A-Level-NEA---Autonomous-Car\car.png").convert()
        self.sprite = pygame.transfom.scale(self.sprite, (carWidth, carHeight))
        self.rotated = self.sprite

        self.position = (0,0) #Starting position not determined yet
        self.angle = 0
        self.speed = 0

        self.speed_set = False

        self.center = [self.position[0]+ carWidth/2, self.position[1] + carHeight/2]

        self.radars = [] 
        self.drawing_radars = []

        self.isAlive = True

        self.distance = 0 #Distance travelled
        self.time = 0 #Time elapsed

    def draw(self, screen):
        screen.blit(self.rotated, self.position) #Blit pygame function draws the sprite on the screen
        self.draw_radar(screen)

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def collision(self, track):
        self.isAlive = True
        for i in self.corners: #For each point on the map
            if track.get_at((int(i[0]), int(i[1]))) == white: #get_at gets the colour value of a single point.
                self.isAlive = False #If this colour value is white, the car will crash.
                break


    def check_radar(self, degree, track):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        while not track.get_at((x, y)) == white and length < 300: #While the car has not hit the edge of the track, the length will increase by 1 which allows it to go further
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        distanceToBorder = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))) #Calculates distance to the edge
        self.radars.append([(x, y), distanceToBorder]) #Appends this distance to the radars (the distance is used as an input in the neural network)

    def update(self, track):
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        self.rotated = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20) #Doesn't let car get closer to 20 pixels of distance away from the edge of the track
        self.position[0] = min(self.position[0], WIDTH - 120)

        self.distance += self.speed #Increases distance
        self.time += 1 #Increases time
        
        
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed #Same as above but for Y position
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

       
        self.center = [int(self.position[0]) + carWidth/2, int(self.position[1]) + carHeight/2] #center changed

        # Calculates four corners
        # Length = 1/2 the side
        length = 0.5 * carWidth
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

       
        self.collision(track) #Checks for collisions
        self.radars.clear() #Clears radars

        for i in range(-90, 120, 45):
            self.check_radar(i, track) #Every 45 degrees from -90 to 120 it checks the radar.

    def grabData(self):
        radars = self.radars
        radar_values = [0,0,0,0,0]
        for i, j in enumerate(radars):
            radar_values[i] = int(j[1]/30)
        return radar_values

    def alive(self):
        return self.isAlive

    def get_reward(self):
        return self.distance/50

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rect = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rect.copy()
        rotated_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rect).copy()
        return rotated_image




pygame.init()


