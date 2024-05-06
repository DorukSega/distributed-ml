from libs.pythonp2pmain.pythonp2p import node
import struct

mtype_list = {
    0x00: 'info',
    0x01: 'math',
    0x02: 'answ',
}

class DMLNode(node.Node):
    def send_bitstream(self, mtype: str, op: int, vars: tuple[int], reciever=None):
        swap_mtypelist = {v: k for k, v in mtype_list.items()}
        mtype_byte = swap_mtypelist[mtype] & 0xFF
        var = bytes()
        for x in vars:
            var += struct.pack('>Q', x)
        msg = (bytes([mtype_byte, op]) + var).hex()
        self.send_message(msg, reciever)

    def math_ops(self, problem, sender):
        if not (
            "mtype" in problem
            and "op" in problem
            and "var" in problem
            and problem["mtype"] == 'math'
        ):
            return

        result = 0
        if problem['op'] == 0x00: # linear func
            result = (problem['var']['w'] * problem['var']['x']) + problem['var']['b']
        
        self.send_bitstream('answ',0x00, (result,), sender)

def parse_bitstream(bstream):
    bstream = bytes.fromhex(bstream)
    result = {}
    mtype = int.from_bytes(bstream[:1],  signed=False)  # 8 bits
    op = int.from_bytes(bstream[1:2], signed=False)  # 8 bits

    result['mtype'] = mtype_list[mtype]
    result['op'] = op
    result['var'] = None

    if mtype_list[mtype] == 'math':
        if op == 0x00:  # linear func
            varstream = bstream[2:]
            var = {
                'w': int.from_bytes(varstream[:8],   signed=False),  # 64 bits
                'x': int.from_bytes(varstream[8:16], signed=False),  # 64 bits
                'b': int.from_bytes(varstream[16:],  signed=False)  # 64 bits
            }
        result['var'] = var

    elif mtype_list[mtype] == 'answ':
        result['var'] = int.from_bytes(bstream[2:], signed=False)

    return result


