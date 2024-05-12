from libs.pythonp2pmain.pythonp2p import node
import struct
import math

mtype_list = {
    0x00: 'info',
    0x01: 'math',
    0x02: 'answ',
}

valuetype_list ={
    0x00: 'uint64',
    0x01: 'int64',
    0x02: 'float64',
}

class DMLNode(node.Node):
    def send_bitstream(self, mtype: str, op: int, vars: tuple[int], reciever=None):
        swap_mtypelist = {v: k for k, v in mtype_list.items()}
        mtype_byte = swap_mtypelist[mtype] & 0xFF
        var = bytes()
        for x in vars:
            if type(x) is int and x >= 0: 
                var += struct.pack('>b', 0x00)
                var += struct.pack('>Q', x)
            elif type(x) is int and x < 0: 
                var += struct.pack('>b', 0x01)
                var += struct.pack('>Q', x)
            elif type(x) is float:
                var += struct.pack('>b', 0x02)
                var += struct.pack('>d', x)
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
        elif problem['op'] == 0x03: # tanh
            result = math.tanh(problem['var']['x'])
        self.send_bitstream('answ',0x00, (result,), sender)

def parse_bitstream(bstream):
    bstream = bytes.fromhex(bstream)
    result = {}
    mtype = int.from_bytes(bstream[:1],  signed=False)  # 8 bits
    op = int.from_bytes(bstream[1:2], signed=False)  # 8 bits

    result['mtype'] = mtype_list[mtype]
    result['op'] = op
    result['var'] = None

    varstream = bstream[2:]
    var = {}
    if mtype_list[mtype] == 'math':
      
        if op == 0x00:  # linear func
            for val in ['w','x','b']:
                var[val] = parse_value(varstream) 
                varstream = varstream[9:]

        elif op == 0x03: # tanh
            var = {
                'x': parse_value(varstream),  # 64 bits
            }

        result['var'] = var

    elif mtype_list[mtype] == 'answ':
        result['var'] = parse_value(varstream)

    return result


def parse_value(valstream: bytes):
    sign = int.from_bytes(valstream[:1],  signed=False)
    if valuetype_list[sign] == 'uint64':
        result = int.from_bytes(valstream[1:9],   signed=False)
    elif valuetype_list[sign] == 'int64':
        result = int.from_bytes(valstream[1:9],   signed=True)
    elif valuetype_list[sign] == 'float64':
        result = struct.unpack('>d', valstream[1:9])[0]
    else:
        print("Unsupported Type")
        return
    return result