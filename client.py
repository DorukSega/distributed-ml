import socket
import threading
import json
from ML import forward_pass
from network import receive_full, pack_message, is_port_in_use


class Client:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        while is_port_in_use(port):
            port += 1
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect_to_server(self, host, port):
        try:
            self.client_socket.connect((host, port))
            print("Connected to the server")
            self.connected = True
            threading.Thread(target=self.receive_messages).start()
        except ConnectionRefusedError:
            print("Failed to connect to the server")

    def receive_messages(self):
        while self.connected:
            message = receive_full(self.client_socket)
            self.handle_ML(message)
            
    def send_message(self, message):
        packed = pack_message(message)
        self.client_socket.send(packed)

    def handle_ML(self, message):
        reciever = message['reciever']
        activation = message['activation']
        pgroup = message['pgroup']
        inode = message['id']
        outputs = []
        for problem in pgroup:
            weights = problem['weights'],
            bias = problem['bias'],
            inputs = problem['inputs']
            output = forward_pass(weights, inputs, bias, activation)
            outputs.append(output[0][0])
        print(f"{inode}, {activation}: {len(pgroup)}")
        self.send_message({'outputs': outputs, 'id': inode})

    def get_selfaddress(self):
        sock_adr = client.client_socket.getsockname()
        return ":".join(map(str, sock_adr))

    def stop_client(self):
        self.client_socket.close()
        print("Client stopped")

if __name__ == "__main__":
    client = Client()
    while True:
        try:
            inp = input()
        except KeyboardInterrupt:
            client.stop_client()
            exit(0)

        if inp.startswith('c'):
            parts = inp.split()
            if len(parts) == 3:
                ip = parts[1]
                port = int(parts[2])
                client.connect_to_server(ip, port)
            else:
                client.connect_to_server('127.0.0.1', 50000)
        elif inp == 'x':
            break