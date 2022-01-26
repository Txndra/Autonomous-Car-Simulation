import sys
import numpy as np
import matplotlib.pyplot as plt #I only added this so I could see what the sigmoid function looked like
from numpy.ma.core import outerproduct

class Neural:
    def __init__(self):
        #determine sizes for feed forward nn
        self.inputLayerSize = 4
        self.hiddenLayer1Size = 5
        self.hiddenLayer2Size = 5
        self.outputLayerSize = 2

        #randomises weights
        self.weights1 = np.random.randn(self.inputLayerSize, self.hiddenLayer1Size) 
        self.weights2 = np.random.randn(self.hiddenLayer1Size, self.hiddenLayer2Size)
        self.weights3 = np.random.randn(self.hiddenLayer2Size, self.outputLayerSize)
        

    def calculateOutput(self, inputs):
        e = np.array([inputs]) #puts inputs into an array
        output = self.forward(e)[0] #determines outputs
        angle = output[0]
        if angle > 0.6:
            angleChange = -2
        elif angle < 0.4:
            angleChange = 2
        else:
            angleChange = 0
        #changes angle based on the neural network's output for the first output neuron
        acceleration = output[1]
        #acceleration changes based on the second output neuron
        return(angleChange, acceleration)


    def forward(self, e):
        #Traverses through neural network using matrix multiplication to find an output
        hidden1 = np.matmul(e, self.weights1)
        activated1 = self.sigmoid(hidden1)
        hidden2 = np.matmul(e, self.weights2)
        activated2 = self.sigmoid(hidden2)
        hidden3 = np.matmul(e, self.weights3)
        activated3 = self.sigmoid(hidden3)

        return activated3  
        #This function uses matrix multiplication and the sigmoid function (which ranges from 0 to 1) as the activation function

    def sigmoid(self, x):
        return 1/(1 + np.exp(-x)) #this is the sigmoid function (returns values between 0 and 1). 
        #it is just a rescalement and translation of the hyperbolic tan function (e^2x-1)/(e^2x+1)so it ranges from 0 to 1



