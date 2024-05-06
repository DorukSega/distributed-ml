from libs.pythonp2pmain.pythonp2p import node
from network import *


class ClientNode(DMLNode):
    def on_message(self, message, sender, private):
        parsed = parse_bitstream(message)
        print(parsed)
        self.math_ops(parsed, sender)


client = ClientNode("127.0.0.1", 65435, 65437)

client.start()

while 1:
    inp = input()
    if inp == 'c':
        client.connect_to("127.0.0.1", 65434)
    elif inp == 'x':
        break

client.stop()