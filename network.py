import json
import socket
import struct

def receive_full(sock: socket.socket, buffer_size=20000):
    # First receive the uint64 bit size (8 bytes)
    size_data = sock.recv(8)
    if len(size_data) < 8:
        raise ValueError("Failed to receive the size of the message")

    size = struct.unpack('!Q', size_data)[0]

    buffer = b""
    while len(buffer) < size:
        data = sock.recv(min(buffer_size, size - len(buffer)))
        if not data:
            raise ValueError("Connection closed before the complete message was received")
        buffer += data

    message = buffer.decode('utf-8')

    try:
        json_message = json.loads(message)
        return json_message
    except json.JSONDecodeError:
        raise ValueError("Received data is not a valid JSON")


def pack_message(message:dict) -> bytes:
    json_message = json.dumps(message)
    encoded = json_message.encode('utf-8')
    size = len(encoded)
    # Ensure the size fits within 64 bits (8 bytes)
    size_bytes = struct.pack('!Q', size)
    bytestream = size_bytes + encoded
    return bytestream

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
        except socket.error as e:
            if e.errno == socket.errno.EADDRINUSE:
                return True
            else:
                return False
        return False
