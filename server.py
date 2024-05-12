from libs.pythonp2pmain.pythonp2p import node
from network import *


class Mynode(DMLNode):
    def on_message(self, message, sender, private):
        parsed = parse_bitstream(message)
        print(parsed)


server = Mynode("127.0.0.1", 65434, 65436)

server.start()
cur_nodes = 0
while 1:
    if len(server.nodes_connected) > cur_nodes:
        cur_nodes+=1
        print("[SERV] New node connected")

    inp = input()
    if inp.startswith('sm'):
        inpl = inp.split()
        server.send_bitstream('math', int(inpl[1]), tuple(int(x) for x in inpl[2:]) )