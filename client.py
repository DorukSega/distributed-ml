from libs.pythonp2pmain.pythonp2p import node
import struct

class Mynode(node.Node):
  def on_message(self, message, sender, private):
    if not private:
        pass # message to announce host?
    if private:
        print(message)
        pass # math problem


client = Mynode("127.0.0.1", 65435, 65437)

client.start()

client.connect_to("127.0.0.1", 65434)


client.send_message(struct.pack('>BI', 0xA, 0b11001010))

