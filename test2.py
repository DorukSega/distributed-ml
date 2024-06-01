from libs.pythonp2pmain.pythonp2p import node
import struct

class Mynode(node.Node):
  def on_message(self, message, sender, private):
     print(f"{message}")
    


node0 = Mynode("127.0.0.1", 65434, 65436)
node1 = Mynode("127.0.0.1", 65435, 65437)

node0.start()
node1.start()

node0.connect_to("127.0.0.1", 65435)

node0.send_message("TEST MESSAGE 1")

print("Connected nodes: ")
print(node0.nodes_connected[0].id == node1.nodes_connected[0].id)

node0.send_message("test", reciever=node1.id)