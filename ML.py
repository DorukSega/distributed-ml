import random
import math

activation_functs = {
    'linear': lambda x: x,
    'sigmoid': lambda x: 1 / (1 + math.exp(-x)),
    'relu': lambda x: x if x > 0 else 0,
    'tanh': lambda x: math.tanh(x),
    'softplus': lambda x: math.log1p(math.exp(x))
}

activation_functs_derivatives = {
    'linear': lambda x: 1,
    'sigmoid': lambda x: (lambda s: s * (1 - s))(1 / (1 + math.exp(-x))),
    'relu': lambda x: 1 if x > 0 else 0,
    'tanh': lambda x: 1 - math.tanh(x) ** 2,
    'softplus': lambda x: 1 / (1 + math.exp(-x))
}

class Neuron:
    def __init__(self, nin, a_type='linear', _children=()):
        self.W = [random.uniform(-1,1) for _ in range(nin)]
        self.b = 0
        self.activation_type = a_type
        self.grad = 0
        self._backward = lambda: None   #takes grad from previous and give the next one
        self._prev = set(_children)     # previously used variables memory

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
    
    #WILL CHANGE copy from micrograd
    def backward(self):

        # topological order all of the children in the graph
        topo = []
        visited = set()
        # object list unordered collection of unique object

        #topo sort all edges goes left to right one way
        # goes all children than add itself
        def build_topo(v):
            if v not in visited:
            # go each unique item
                visited.add(v)
                # add objects to object list
                for child in v._prev:
                    # repeat for each child 
                    #and make bottom to top list
                    build_topo(child)
                topo.append(v)
                # append each with childrens

        build_topo(self)

        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()



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


    def train_normal(self, X_train, y_train, learning_rate, epochs=1):
        for epoch in range(epochs):
            total_loss = 0
            for X, y in zip(X_train, y_train):
                output = X # input
                for layer in self.layers:
                    ###
                    output = [neuron.forward(output) for neuron in layer.neurons]
                    ###

                ### compute loss, can be split
                loss = [(o - yt)**2 for o, yt in zip(output, y)]
                total_loss += sum(loss)/ len(loss)
                #new weight = weight old - (derivate loss/ derivative weight) * learning rate
                #derivate loss/ derivative weight =
                #derivate (loss) + derivate(activation) + derivate(weight) 

                # Backward pass
                reversed_layers = list(self.layers)
                reversed_layers.reverse()
                # for i, layer in enumerate(reversed_layers):
                #     neuron.backward(loss,)

                # Update weights
                # for layer in self.layers:
                #     for neuron in layer.neurons:
                #         neuron.update_weights(learning_rate)

            ## print loss every epoch
            print("Epoch:", epoch + 1, "Loss:", total_loss)