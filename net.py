import numpy as np

import calc

# Base class
class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward_propagation(self, input):
        raise NotImplementedError
        
        
# Fully Connected Layer
class FCLayer(Layer):
    # input_size = number of input neurons
    # output_size = number of output neurons
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # makes random changes to neuron weights and biases
    def evolve(self, evolution_rate):
        for i, weight in enumerate(self.weights):
            self.weights[i] = calc.applyEvolution(self.weights[i], evolution_rate)
        for i, bias in enumerate(self.bias):
            self.bias[i] = calc.applyEvolution(self.bias[i], evolution_rate)
    
    
# Activation Layer
class ActivationLayer(Layer):
    def __init__(self, activation, activation_prime):
        self.activation = activation
        self.activation_prime = activation_prime

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output

    def evolve(self, evolution_rate):
        pass

    
# activation function and its derivative
def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1-np.tanh(x)**2

# derivative is the same for relu
def relu(x):
    return np.maximum(0, x)

# for hidden layer that does not change data
def direct(x):
    return x


class Network:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_prime = None

    # add layer to network
    def add(self, layer):
        self.layers.append(layer)

    def evolve(self, evolution_rate):
        for layer in self.layers:
            layer.evolve(evolution_rate)

    # predict output for given input
    def predict(self, input_data):

        output = input_data

        # forward propagation
        for layer in self.layers:
            output = layer.forward_propagation(output)

        return output[0]