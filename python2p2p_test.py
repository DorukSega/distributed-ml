from libs.pythonp2pmain.pythonp2p import node
import struct

class Mynode(node.Node):
  def on_message(self, message, sender, private):
    if not private:
        print(message)
        pass # message to announce host?
    if private:
        print(message)
        pass # math problem


node0 = Mynode("127.0.0.1", 65434, 65436)
node1 = Mynode("127.0.0.1", 65435, 65437)

node0.start()
node1.start()

node0.connect_to("127.0.0.1", 65435)

node0.send_message("TEST MESSAGE 1")

print("Connected nodes: ")
print(node0.nodes_connected)
print(node1.nodes_connected)


node0.send_message(struct.pack('>BI', 0xA, 0b11001010).hex(), reciever=node1.id)


# node0.stop()
# node1.stop()
