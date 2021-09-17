import math
import random
import sys
import os

import neat
import pygame
from pygame.locals import *


WIDTH = 800
HEIGHT = 600

carWidth = 60
carHeight = 60 

wallColour = (255,0,0) #If car touches this colour it will crash
blue = (0,0,255) #For drawing radars

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
            pygame.draw.line(screen, (0, 0, 255), self.center, position, 1)
            pygame.draw.circle(screen, (0, 0, 255), position, 5)

    def collision(self, track):
        self.isAlive = True
        for i in self.corners: #For each point on the map
            if track.get_at((int(i[0]), int(i[1]))) == wallColour: #get_at gets the colour value of a single point.
                self.isAlive = False #If this colour value is wallColour, the car will crash.
                break


    def check_radar(self, degree, track):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        while not track.get_at((x, y)) == wallColour and length < 300: #While the car has not hit the edge of the track, the length will increase by 1 which allows it to go further
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





def run_simulation(genomes, config):
    
    # Empty Collections For Nets and Cars
    nets = []
    cars = []
    global WIDTH
    global HEIGHT 
    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    track = pygame.image.load(r"C:\Users\sdgam\OneDrive\Documents\AUTONOMOUS CARSIM\A-Level-NEA---Autonomous-Car\A-Level-NEA---Autonomous-Car\map1.png").convert() # Convert Speeds Up A Lot

    global generation
    generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.grabData())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10 # Left
            elif choice == 1:
                car.angle -= 10 # Right
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2 # Slow Down
            else:
                car.speed += 2 # Speed Up
        
        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(track)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40: # Stop After About 20 Seconds
            break

        # Draw Map And All Cars That Are Alive
        screen.blit(track, (0, 0))
        for car in cars:
            if car.isAlive():
                car.draw(screen)
        
        # Display Info
        text = generation_font.render("Generation: " + str(generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60) # 60 FPS

if __name__ == "__main__":
    
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)

