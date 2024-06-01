from libs.pythonp2pmain.pythonp2p import node
from network import *
from ML import forward_pass

import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
        except socket.error as e:
            if e.errno == socket.errno.EADDRINUSE:
                return True
            else:
                return False
        return False


class ClientNode(DMLNode):
    def on_message(self, message, sender, private):
        activation = message['activation']
        pgroup = message['pgroup']
        inode = message['id']
        outputs = []
        for problem in pgroup:
            weights= problem['weights'],
            bias = problem['bias'],
            inputs = problem['inputs']
            output = forward_pass(weights, inputs, bias, activation)
            outputs.append(output[0][0])
        print(f"solving {activation}")
        self.send_message({'outputs':outputs, 'id': inode}, sender)


port = 65435
file_port = 65437
while is_port_in_use(port) or is_port_in_use(file_port):
    port+=1
    file_port+=1

client = ClientNode("127.0.0.1", port, file_port)
client.start()

while 1:
    inp = input()
    if inp == 'c':
        for _ in range(10):
            client.connect_to("127.0.0.1", 50000)
    elif inp == 'x':
        break

client.stop()