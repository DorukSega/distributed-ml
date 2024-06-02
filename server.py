from libs.pythonp2pmain.pythonp2p import node
from network import *
from ML import *
import time

class ServerNode(DMLNode):
    def on_message(self, message, sender, private):
        id = message['id'] 
        self.solutions[id] = message['outputs']
       

if __name__ == "__main__":
    server = ServerNode("127.0.0.1", 50000, 50001)

    server.start()

    # XOR
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_train = np.array([[0], [1], [1], [0]])

    while 1:
        inp = input()
        if inp.startswith('sm'):
            start_dis = time.time()
            model = MLP([
                    Layer('relu', 8, input_shape=2),  
                    Layer('relu', 8),
                    Layer('sigmoid', 1)                
            ], net=server)
            loss = model.train(X_train, y_train, learning_rate=0.1, epochs=100)
            end_dis = time.time()
            print(f"time: {end_dis - start_dis:.4f}s")
            print("Test Predictions:")
            for X in X_train:
                prediction = model.predict(X)
                print(f"Input: {X}, Predicted: {prediction[0]}")

        elif inp.startswith('n'):
            print(f"[SERV] nodes {len(server.nodes_connected)}")

