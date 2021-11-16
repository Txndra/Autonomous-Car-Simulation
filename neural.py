import sys
import numpy as np
import matplotlib.pyplot as plt

class Neural:
    def __init__(self):
        self.inputLayerSize = 4
        self.outputLayerSize = 2

        self.weights1 = np.random.randn(self.inputLayerSize, self.outputLayerSize) #randomises weights

    def calculateOutput(self, inputs):
        e = np.array([inputs])
        output = self.forward(e)[0] #determines outputs
        angle = output[0]
        if angle > 0.6:
            angleChange = -2
        elif angle < 0.4:
            angleChange = 2
        else:
            angleChange = 0

        acceleration = output[1]

        return(angleChange, acceleration)


    def forward(self, X): #Traverses through neyral network using matrix multiplication to find an output
        pass

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))


