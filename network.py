from libs.pythonp2pmain.pythonp2p import node
import struct
import math

mtype_list = {
    0x00: 'info',
    0x01: 'math',
    0x02: 'answ',
}

math_op_list = {
    0x00: 'linear',
    0x01: 'sigmoid',
    0x02: 'relu',
    0x03: 'tanh'
}

valuetype_list ={
    0x00: 'uint64',
    0x01: 'int64',
    0x02: 'float64',
}


class PackageOLD:
    def __init__(self, mtype: str, op: int, vars: tuple[int]):
        self.mtype = mtype
        self.op = op
        self.vars = vars

    def pack(self):
        swap_mtypelist = {v: k for k, v in mtype_list.items()}
        mtype_byte = swap_mtypelist[self.mtype] & 0xFF
        var = bytes()
        for x in self.vars:
            if type(x) is int and x >= 0: 
                var += struct.pack('>b', 0x00)
                var += struct.pack('>Q', x)
            elif type(x) is int and x < 0: 
                var += struct.pack('>b', 0x01)
                var += struct.pack('>Q', x)
            elif type(x) is float:
                var += struct.pack('>b', 0x02)
                var += struct.pack('>d', x)
        return bytes([mtype_byte, self.op]) + var
        
class Box:
    def __init__(self, mtype: str, op: int, var: dict):
        self.mtype = mtype
        self.op = op
        self.var = var
    
    def math_ops(self):
        if not (
            "mtype" in self
            and "op" in self
            and "var" in self
            and self["mtype"] == 'math'
        ):
            return

        result = 0
        if self.op == 0x00: # linear func
            result = (self['var']['w'] * self['var']['x']) + self['var']['b']
        elif self['op'] == 0x03: # tanh
            result = math.tanh(self['var']['x'])
        return result

class DMLNode(node.Node):
    # pid 8bit | pcount 8bit | packages
    def send_package(self, pid: int, packages: list[PackageOLD], reciever=None):
        msg = bytes([(pid & 0xFF), (len(packages) & 0xFF)])
        for package in packages:
            msg += package.pack()
        self.send_message(msg.hex(), reciever)
        
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
    
    pid = int.from_bytes(bstream[:1],  signed=False) # 8 bit
    pcount = int.from_bytes(bstream[1:2], signed=False)  # 8 bits
    result = {
        'pid':      pid,
        'pcount':   pcount,
        'packages': [], 
    }

    for k in range(pcount):
        pstream = bstream[2:]

        mtype = int.from_bytes(pstream[:1],  signed=False)  # 8 bits
        op = int.from_bytes(pstream[1:2], signed=False)  # 8 bits
        
        varstream = pstream[2:]
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
        elif mtype_list[mtype] == 'answ':
            var = parse_value(varstream)

        result['packages'][k] = Box(
            mtype= mtype_list[mtype],
            op = op,
            var= var
        ) 

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