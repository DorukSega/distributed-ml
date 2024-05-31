from ML import *
import numpy as np

# XOR
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([[0], [1], [1], [0]])

# Train the model
loss = 1
while loss > 0.1:
    model = MLP([
        Layer('relu', 2, input_shape=2),  # Input layer with ReLU activation
        Layer('relu', 4),
        Layer('sigmoid', 1)                # Output layer with Sigmoid activation
    ])
    loss = model.train(X_train, y_train, learning_rate=0.1, epochs=5000)

# Test the trained model
print("Test Predictions:")
for X in X_train:
    prediction = model.predict(X)
    print(f"Input: {X}, Predicted Output: {prediction[0]}")
