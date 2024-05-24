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
model.train_normal()