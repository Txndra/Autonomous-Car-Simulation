from neural import Neural
import pygame
from pygame.math import Vector2
from prototype import CAR_SIZE_X, CAR_SIZE_Y

class Car:
    beamAngles = [-45, 0, 45] #angles for the car beams
    carSize = None
    beamCarOffset = 10
    idCounter = 0
    CAR_SIZE_X = 20
    CAR_SIZE_Y = 20
    def __init__(self):
        self.id = Car.idCounter
        Car.idCounter += 1

        self.brain = Neural() # Assigns neural network to car
        self.framesAlive = 0
        self.fitness = 0
        self.dead = False

        self.bestCar = False
        self.collidedCheckPoints = []
        self.sprite = pygame.image.load(r"car.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]
        self.rotated_sprite = self.sprite

        self.angle = 0
        self.speed = 0
        self.radars = []
        self.drawing_radars = []
        
        def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
            for radar in self.radars:
                position = radar[0]
                pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
                pygame.draw.circle(screen, (0, 255, 0), position, 5)



