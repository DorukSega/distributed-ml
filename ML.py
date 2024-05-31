import numpy as np


# Define activation functions and their derivatives
activation_functions = {
    'relu': (lambda x: np.maximum(0, x), lambda x: np.where(x > 0, 1, 0)),
    'sigmoid': (lambda x: 1 / (1 + np.exp(-x)), lambda x: x * (1 - x))
}

def forward_net(W, X, b, activation):
    W = np.array(W)
    X = np.array(X)
    b = np.array(b)
    z = np.dot(W, X) + b
    f_activation, _ = activation_functions[activation]
    a = f_activation(z)
    return a

def split_array(arr: list, n):
    assert n > 0 # Number of groups should be greater than zero
    if n > len(arr):
        n_big = n
        n = len(arr)
    group_size = len(arr) // n
    remainder = len(arr) % n
    groups = [arr[i * group_size + min(i, remainder):(i + 1) * group_size + min(i + 1, remainder)] for i in range(n)]
    return groups 

class Neuron:
    def __init__(self, n_inputs, activation):
        self.weights = np.random.randn(n_inputs)
        self.bias = np.random.randn()
        self.activation_type = activation
        self.activation, self.activation_derivative = activation_functions[activation]
    
    def backward(self, dvalue):
        self.dactivation = self.activation_derivative(self.output) * dvalue
        self.dweights = self.inputs * self.dactivation
        self.dbias = self.dactivation
        self.dinputs = self.dactivation * self.weights
        return self.dinputs

    def update(self, learning_rate):
        self.weights -= learning_rate * self.dweights
        self.bias -= learning_rate * self.dbias
        
    def __repr__(self):
        return (f"<Neuron>")
            
class Layer:
    def __init__(self, activation, n_neurons, input_shape=None, net=False):
        self.activation = activation
        self.n_neurons = n_neurons
        self.input_shape = input_shape
        self.neurons = []
        self.net = net
    
    def initialize(self, input_shape):
        self.neurons = [Neuron(input_shape, self.activation) for _ in range(self.n_neurons)]
    
    def forward(self, inputs):
        self.inputs = np.array(inputs)
        outputs = []
    
        if self.net:
            # TODO: add networking !!
            client_count = 2
            neuron_groups = split_array(self.neurons, client_count)
            for group in neuron_groups:
                group_outputs = []
                for neuron in group:
                    neuron.inputs = np.array(inputs)
                    neuron.output = forward_net(neuron.weights, inputs, neuron.bias, self.activation)
                    group_outputs.append(neuron.output)
                outputs+= group_outputs
        else:
            for neuron in self.neurons:
                neuron.inputs = np.array(inputs)
                neuron.output = forward_net(neuron.weights, inputs, neuron.bias, self.activation)
                outputs.append(neuron.output)
        self.outputs = np.array(outputs)
        return self.outputs
    
    def backward(self, dvalues):
        dvalues = np.array(dvalues)
        dinputs = np.zeros(self.inputs.shape)
        for i, neuron in enumerate(self.neurons):
            dinputs += neuron.backward(dvalues[i])
        return dinputs
    
    def update(self, learning_rate):
        for neuron in self.neurons:
            neuron.update(learning_rate)

class MLP:
    def __init__(self, layers, net=False):
        self.layers = layers
        self.net = net
        for i, layer in enumerate(self.layers):
            layer.net = net
            input_shape = self.layers[i-1].n_neurons if i > 0 else layer.input_shape
            layer.initialize(input_shape)
    
    def forward(self, inputs):
        for layer in self.layers:
            inputs = layer.forward(inputs)
        return inputs
    
    def backward(self, y_true):
        dvalue = self.output - y_true
        for layer in reversed(self.layers):
            dvalue = layer.backward(dvalue)
    
    def train(self, X_train, y_train, learning_rate, epochs):
        for epoch in range(epochs):
            total_loss = 0
            for inputs, y_true in zip(X_train, y_train):
                self.output = self.forward(inputs)
                loss = np.mean((self.output - y_true) ** 2)
                total_loss += loss
                self.backward(y_true)
                for layer in self.layers:
                    layer.update(learning_rate)
            avg_loss = total_loss / len(X_train)
            if epoch % 100 == 0:
                print(f'Epoch {epoch}, Loss: {avg_loss:.4f}')
        return avg_loss
    
    def predict(self, inputs):
        return self.forward(inputs)

