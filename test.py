import ML

# ner = ML.Neuron(1)

# z = ner(5)
# print("W:", ner.W)
# print("b:", ner.b)
# print(z)

X_train = [[0, 0], [0, 1], [1, 0], [1, 1]]
y_train = [[0], [1], [1], [0]]

# Create MLP model
model = ML.MLP([
    ML.Dense('relu', 2, input_shape=2),  # Input layer with ReLU activation
    ML.Dense('sigmoid', 1)                # Output layer with Sigmoid activation
])

# Train the model
model.train_normal(X_train, y_train, learning_rate=0.1, epochs=1000)

# Test the trained model
print("Test Predictions:")
for X in X_train:
    prediction = model.forward(X)
    print(f"Input: {X}, Predicted Output: {prediction}")