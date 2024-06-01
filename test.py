from ML import *
import numpy as np
import time

# XOR
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_train = np.array([[0], [1], [1], [0]])

start_nodis = time.time()
# Train the model
loss = 1
while loss > 0.1:
    model = MLP([
        Layer('relu', 4, input_shape=2),  # Input layer with ReLU activation
        Layer('relu', 4),
        Layer('sigmoid', 1)                # Output layer with Sigmoid activation
    ])
    loss = model.train(X_train, y_train, learning_rate=0.1, epochs=5000)
end_nodis = time.time()

start_dis = time.time()
loss = 1
while loss > 0.1:
    model = MLP([
        Layer('relu', 4, input_shape=2),  
        Layer('relu', 4),
        Layer('sigmoid', 1)                
    ], False)
    loss = model.train(X_train, y_train, learning_rate=0.1, epochs=5000)
end_dis = time.time()

print(f"not dis: {end_nodis - start_nodis:.4f}s, dis: {end_dis - start_dis:.4f}s")

# Test the trained model
print("Test Predictions:")
for X in X_train:
    prediction = model.predict(X)
    print(f"Input: {X}, Predicted: {prediction[0]}")
