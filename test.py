import ML

ner = ML.Neuron(1)

z = ner(5)
print("W:", ner.W)
print("b:", ner.b)
print(z)