import socket
import threading
import json
import time
import typing
import numpy as np
from ML import MLP, Layer

class Server:
    def __init__(self, host='127.0.0.1', port=50000):
        self.host = host
        self.port = port
        self.clients: typing.Dict[str, socket.socket] = {}
        self.running = True

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")
        self.accept_thread = threading.Thread(target=self.accept_clients)
        self.accept_thread.start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(
                    f"Connection from {client_address} has been established.")
                address = ":".join(map(str, client_address))
                self.clients[address] = client_socket
                threading.Thread(target=self.handle_client,
                                 args=(client_socket, address)).start()
            except socket.error:
                break
            except KeyboardInterrupt:
                server.stop_server()
                exit(0)

    def handle_client(self, client_socket, address):
        while self.running:
            # try:
            message = client_socket.recv(200000).decode('utf-8')
            self.handle_ML(json.loads(message))
            # except:
            #     self.clients.pop(address)
            #     client_socket.close()
            #     break

    def broadcast(self, message, client_socket, address):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.clients.pop(address)
                    client.close()

    def send_message(self, message, address=None):
        json_message = json.dumps(message)
        for cl_address, client in self.clients.items():
            if not address:
                client.send(json_message.encode('utf-8'))
            elif address and cl_address == address:
                client.send(json_message.encode('utf-8'))

    def handle_ML(self, message):
        id = message['id']
        self.solutions[id] = message['outputs']

    def stop_server(self):
        self.running = False
        for _, client in self.clients.items():
            client.close()
        self.server_socket.close()
        self.accept_thread.join()
        print("Server stopped")

    def get_addresses(self):
        return list(self.clients.keys())


if __name__ == "__main__":
    # XOR
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_train = np.array([[0], [1], [1], [0]])

    server = Server()
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()

  
    while 1:
        try:
            inp = input()
        except KeyboardInterrupt:
            server.stop_server()
            
        if inp.startswith('sm'):
            model_skeleton = [
                    Layer('relu', 8, input_shape=2),
                    Layer('relu', 8),
                    Layer('sigmoid', 1)
                ]
            # Distrubuted test
            start_dis = time.time()
            model_dis = MLP(model_skeleton, net=server)
            model_dis.train(X_train, y_train, learning_rate=0.1, epochs=1000)
            end_dis = time.time()

            print("DIS pred:")
            for X in X_train:
                prediction = model_dis.predict(X)
                print(f"{X} -> {1 if prediction[0] >= 0.5 else 0}")

            print("Starting Non Distrubuted")
            time.sleep(1)

            # Not Distrubuted test
            start_time = time.time()
            model_ndis = MLP(model_skeleton)
            model_ndis.train(X_train, y_train, learning_rate=0.1, epochs=1000)
            end_time = time.time()

            print("NotDIS pred:")
            for X in X_train:
                prediction = model_ndis.predict(X)
                print(f"{X} -> {1 if prediction[0] >= 0.5 else 0}")

                
            print(f"notdis time: {end_time - start_time:.4f}s")
            print(f"dis time: {end_dis - start_dis:.4f}s")

        elif inp.startswith('n'):
            print(f"[SERV] nodes {len(server.clients)}")
        elif inp.startswith("e"):
            server.stop_server()