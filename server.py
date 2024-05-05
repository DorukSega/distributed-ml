from libs.pythonp2pmain.pythonp2p import node
import struct

class Mynode(node.Node):
  def on_message(self, message, sender, private):
    if not private:
        print(struct.unpack('>BI',message))
        pass # message to announce host?
    if private:
        print(struct.unpack('>BI',message))
        pass # math problem


main_node = Mynode("127.0.0.1", 65434, 65436)

main_node.start()


print("Connected nodes: ")
print(main_node.nodes_connected)


