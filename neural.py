import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.core import outerproduct

class Neural:
    def __init__(self):
        self.inputLayerSize = 4
        self.hiddenLayer1Size = 5
        self.hiddenLayer2Size = 5
        self.outputLayerSize = 2

        self.weights1 = np.random.randn(self.inputLayerSize, self.hiddenLayer1Size)
        self.weights2 = np.random.randn(self.hiddenLayer1Size, self.hiddenLayer2Size)
        self.weights3 = np.random.randn(self.hiddenLayer2Size, self.outputLayerSize)
           #randomises weights

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


    def forward(self, e): #Traverses through neyral network using matrix multiplication to find an output
        hidden1 = np.matmul(e, self.weights1)
        activated1 = self.sigmoid(hidden1)
        hidden2 = np.matmul(e, self.weights2)
        activated2 = self.sigmoid(hidden2)
        hidden3 = np.matmul(e, self.weights3)
        activated3 = self.sigmoid(hidden3)

        return activated3  
        #This function uses matrix multiplication and the sigmoid function (which ranges from 0 to 1) as the activation function

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))


instant = Neural()
instant.calculateOutput()