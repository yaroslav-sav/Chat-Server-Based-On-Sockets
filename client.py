import socket

import protocol
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8080))

def one_task():
    Username = input("Username: ")
    protocol.send_message(s, "JOIN", Username)
    while True:
        command = input()
        if command == "QUIT":
            break
        message = input()
        protocol.send_message(s, command, message)



def two_task():
    while True:
        try:
            command, payload = protocol.recv_message(s)
        except OSError:
            break
        if command == "QUIT":
            break
        print(f"{command}: {payload}")


t1 = threading.Thread(target=one_task)
t2 = threading.Thread(target=two_task)

t1.start()
t2.start()

t1.join()
t2.join()

s.close()