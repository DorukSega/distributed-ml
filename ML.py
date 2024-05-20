import random
import math

class Neuron:
    def __init__(self, nin, a_type='linear'):
        self.W = [random.uniform(-1,1) for _ in range(nin)]
        self.b = 0
        self.activation_type = a_type

    def linear(self, X):
        return sum((wi*xi for wi,xi in zip(self.W, X)), self.b) # w*x + b

    def __call__(self, X):
        if type(X) != list:
            X = [X]
            
        z = self.linear(X)

        if self.activation_type == 'linear':
            return z * 1.0 # result
        else:
            # TODO: check if activation type is false
            return activation_functs[self.activation_type](z) * 1.0

         

def A_relu(z):
    return max(0, z)

def A_tanh(z):
    return math.tanh(0, z) 

activation_functs = {
    'relu': A_relu,
    'tanh': A_tanh,
}

