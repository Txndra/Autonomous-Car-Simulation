from car import Car
import random
from CT import CT
import numpy as np

class Population:
    def __init__(self, numCars, frontPoint, carSize, mutationLevel):
        Car.setSize(carSize) #sets size of car

        self.bestCarFitness = 0 #initialises variable for car fitness (so that it can be used for future generations)
        self.dead = False #Boolean for whether the car is dead or not
        self.startPoint = frontPoint
        self.mutationLevel = mutationLevel
        self.numCars = numCars
        self.generation = 1
        #print(self.mutationLevel)
        self.cars = []

        for _ in range(numCars):
            self.cars.append(Car(frontPoint))

    def createDistribution(self):
        distribution = []
        for c in self.cars:
            for f in range(c.fitness):
                distribution.append(c.id)
        return distribution

    def crossover(weights1, weights2):
        newWeights = np.zeros((weights1.shape[0], weights1.shape[1]))

        for row in range(len(newWeights)):
            for weight in range(len(newWeights[0])):
                ranNum = random.randint(0,1)
                if ranNum == 0:
                    newWeights[row][weight] = weights1[row][weight]
                else:
                    newWeights[row][weight] = weights2[row][weight]

        return newWeights

    def mutate(self, car):
        for i in range(len(car.brain.weights1)):
            for j in range(len(car.brain.weights1[0])):
                randNum = random.randint(0, 100)
                if randNum < self.mutationLevel:
                    car.brain.weights1[i][j] = np.random.randn()

        for i in range(len(car.brain.weights2)):
            for j in range(len(car.brain.weights2[0])):
                randNum = random.randint(0, 100)
                if randNum < self.mutationLevel:
                    car.brain.weights2[i][j] = np.random.randn()

        for i in range(len(car.brain.weights3)):
            for j in range(len(car.brain.weights3[0])):
                randNum = random.randint(0, 100)
                if randNum < self.mutationLevel:
                    car.brain.weights3[i][j] = np.random.randn()
    
    def createNextGeneration(self):
        bestCar = self.cars[0]
        for c in self.cars:
            if c.fitness > bestCar.fitness:
                bestCar = c
        self.generation += 1
        if bestCar.fitness > self.bestCarFitness:
            self.bestCarFitness = bestCar.fitness
        
        newCars = []
        Car.idCounter = 0
        for i in range(self.numCars):
            newCars.append(Car(self.startPoint))

        probDistribution = self.createDistribution()
        for c in newCars:
            parent1 = self.cars[probDistribution[random.randint(0, len(probDistribution) - 1)]]
            parent2 = self.cars[probDistribution[random.randint(0, len(probDistribution) - 1)]]

            c.brain.weights1 = Population.crossover(parent1.brain.weights1, parent2.brain.weights1)
            c.brain.weights2 = Population.crossover(parent1.brain.weights2, parent2.brain.weights2)
            c.brain.weights3 = Population.crossover(parent1.brain.weights3, parent2.brain.weights3)
            self.mutate(c)
        newCars[-1].brain.weights1 = bestCar.brain.weights1
        newCars[-1].brain.weights2 = bestCar.brain.weights2
        newCars[-1].brain.weights3 = bestCar.brain.weights3
        newCars[-1].bestOfPrevGen = True
        self.cars = newCars

    def update(self, borderLines, checkPoints):
        horLines = borderLines[0]
        verLines = borderLines[1]

        for c in self.cars:
            if not c.dead:
                for e in c.edges:
                    for line in horLines:
                        if CT.getIntersectBetweenLineSegments(e, ((line[0],line[2]), (line[1],line[2])) ) is not None:
                            c.dead = True
                            c.fitness = int(((len(c.collidedCheckPoints)**7) + 1)/(c.framesAlive))
                            break
                    if not c.dead:
                        for line in verLines:
                            if CT.getIntersectBetweenLineSegments(e, ((line[2],line[0]), (line[2],line[1])) ) is not None:
                                c.dead = True
                                c.fitness = int(((len(c.collidedCheckPoints)**7) + 1)/(c.framesAlive))
                                break
            if not c.dead:
                for e in c.edges:
                    for cp in checkPoints:
                        if CT.getIntersectBetweenLineSegments(e, cp) is not None:
                            if cp not in c.collidedCheckPoints:
                                c.collidedCheckPoints.append(cp)
            if not c.dead:
                c.update(borderLines)
                
            self.checkDead()
    
    
    def checkDead(self):
        self.dead = True
        for c in self.cars:
            if c.dead == False:
                self.dead = False
                break
    def show(self, screen):
        for c in self.cars:
            if not c.dead:
                c.show(screen)
            
