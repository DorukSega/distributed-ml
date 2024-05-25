import ML

# ner = ML.Neuron(1)

# z = ner(5)
# print("W:", ner.W)
# print("b:", ner.b)
# print(z)

model = ML.MLP([
    ML.Dense('relu', 2, input_shape=1),
    ML.Dense('tanh',1)
])

print(model)
X=[1,0,1]
Y= [0,1,1]
model.train_normal(X,Y,0.01)