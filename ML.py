import random
import math

activation_functs = {
    'linear': lambda x: x,
    'relu': lambda x: max(0, x),
    'sigmoid': lambda x: 1 / (1 + math.exp(-x)),
    'tanh': lambda x: math.tanh(x)
}

activation_functs_derivatives = {
    'linear': lambda x: 1,
    'relu': lambda x: max(0, x),
    'sigmoid': lambda x: (lambda s: s * (1 - s))(1 / (1 + math.exp(-x))),
    'tanh': lambda x: 1 - math.tanh(x) ** 2
}

class Neuron:
    def __init__(self, nin, a_type='linear'):
        self.W = [random.uniform(-1,1) for _ in range(nin)]
        self.b = 0
        self.activation_type = a_type

    def linear(self, X):
        return sum((wi*xi for wi,xi in zip(self.W, X)), self.b) # w*x + b

    def forward(self, X): # forward pass
        if type(X) != list:
            X = [X]
        z = self.linear(X)

        if self.activation_type == 'linear':
            return z * 1.0 # result
        else:
            # TODO: check if activation type is unknown
            return activation_functs[self.activation_type](z) * 1.0

    def backward(self, delta, output):
        derivative = activation_functs_derivatives[self.activation_type](output)
        gradient = delta * derivative
        return [gradient * w for w in self.W], gradient * self.b


class Layer:
    def __init__(self, n_neuron, nin, a_type='linear'):
        self.activation = a_type
        self.size = n_neuron
        self.neurons = [Neuron(nin, a_type) for _ in range(n_neuron)]
        

class Dense:
    def __init__(self, activation, n_neuron, input_shape=None):
        self.n_neuron = n_neuron
        self.activation = activation
        self.input_shape = input_shape
        
class MLP:
    def __init__(self, layers: list[Dense]):
        self.layers: list[Layer] = []
        past_n_neuron = 0
        for dense in layers:
            if not past_n_neuron: # first time
                assert(dense.input_shape != None) 
                self.input_size = dense.input_shape
            if dense.input_shape:
                past_n_neuron = dense.input_shape

            self.layers.append(Layer(dense.n_neuron, past_n_neuron, dense.activation))
            past_n_neuron = dense.n_neuron
    
    def __repr__(self):
        result = "MLP (\n"
        result += f"  input, {self.input_size}\n"
        for layer in self.layers:
            result += f"  {layer.activation}, {layer.size}\n"
        result += ")\n"
        return result

    def forward(self, X):
        output = X
        for layer in self.layers:
            output = [neuron.forward(output) for neuron in layer.neurons]
        return output

    def train_normal(self, X_train, y_train, learning_rate, epochs=1):
        for epoch in range(epochs):
            total_loss = 0
            for X, y in zip(X_train, y_train):
                output = X 
                for layer in self.layers:
                    ###
                    output = [neuron.forward(output) for neuron in layer.neurons]
                    ###

                # Computae loss
                loss = [(o - yt)**2 for o, yt in zip(output, y)]
                total_loss += sum(loss) / len(loss)

                
                # Gradient Descent

                # Update weights and biases
            
               

            ## print loss every epoch
            print(f'Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(X_train)}')