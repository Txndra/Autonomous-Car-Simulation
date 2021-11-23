#This program is used to create the radar beams
import pygame
from pygame.math import Vector2
import math
from CT import CT #imports coordinate toolkit from previous python file

class radars:
    colour = (0, 255, 0) # green beams (by choice)

    def __init__(self, start, angle):
        self.start = start #returns starting position
        self.length = 5
        self.end = (start[0] + 3, start[0] + 4) #so the end starts with a length
        self.angle = angle
        self.startPoint = pygame.math.Vector2(start[0], start[1]) #creates vector for start point
        self.endPoint = pygame.maths.Vector2(start[0] + 50, start[1])

    def update(self, startVector, rotation, lines):
        self.startPoint = startVector
        if rotation > 0:
            self.angle = (self.angle + rotation) % 360 #adds rotation to angle, then mods with 360 so it's between 0 and 360
        else:
            self.angle = (self.angle + rotation) % -360 #if rotation is negative it needs to mod with -360 for the same reason
        self.rotateLine()
        self.calculateBorderIntersection(lines)
        self.length = self.startPoint.distance_to(self.current) #distance_to (from pygame) calculates distance
        
    def show(self, SCR):
        try:
            pygame.draw.aaline(SCR, radars.colour, self.startPoint, self.current, 1) #blits radars onto screen
        except:
            print('Must update then show beam to initialise length')
        
    def rotateLine(self): 
        #rotates radars by specified angle
        self.current = self.startPoint + self.endPoint.rotate(self.angle)

    def calculateBorderIntersection(self, lines):
        horizontalLines = lines[0] #x values on cartesian plane
        verticalLines = lines[1] #y values on cartesian plane

        smallestDistance = 1
        smallestIntersect = None

        for line in horizontalLines:
            intersect = CT.getIntersectBetweenLineSegments((self.startPoint, self.current), ((line[0], line[2]), (line[1], line[2]))) #finds point of intersection using CT class
            if intersect is not None:
                distance = self.startPoint.distance_to(pygame.math.Vector2(intersect[0], intersect[1])) #finds distance between the intersect and the start point
                if distance < smallestDistance: 
                    smallestDistance = distance
                    smallestIntersect = intersect
        for line in verticalLines:
            #repeats the same thing but for vertical lines
            intersect = CT.getIntersectBetweenLineSegments((self.startPoint, self.current), ((line[2], line[0]), (line[2], line[1])))
            if intersect is not None:
                distance = self.startPoint.distance_to(pygame.math.Vector2(intersect[0], intersect[1]))
                if distance < smallestDistance:
                    smallestDistance = distance
                    smallestIntersect = intersect

        try:
            self.current = pygame.math.Vector2(smallestIntersect[0], smallestIntersect[1]) #Vector2 function defines a vector for the intersect (direction and magnitude)
        except:
            pass
        #if there is no smallest intersect it will pass rather than stop the program.
