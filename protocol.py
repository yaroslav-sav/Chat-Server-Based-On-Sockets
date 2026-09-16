import socket
import struct

def recv_exact(sock, size):
    byte = b""
    while len(byte) < size:
        data = sock.recv(size - len(byte))
        if data == b"":
            raise ConnectionError()
        byte += data
    return byte

commands = {
    "JOIN": 1,
    "TEXT": 2,
    "LIST": 3,
    "QUIT": 4
}
commands_reverse = {
    1: "JOIN",
    2: "TEXT",
    3: "LIST",
    4: "QUIT",
}

def send_message(sock, command: str, payload: bytes):
    if command not in commands:
        raise ValueError()
    head = struct.pack("!II", commands[command], len(payload))
    sock.sendall(head + payload)

def recv_message(sock):
    MAX_MESSAGE_SIZE = 10 * 1024 * 1024
    command, size = struct.unpack("!II", recv_exact(sock, 8))
    if size > MAX_MESSAGE_SIZE:
        raise ValueError()
    if command not in commands_reverse:
        raise ValueError()
    payload = recv_exact(sock, size)
    return commands_reverse[command], payload