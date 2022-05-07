
import socket

adapter_addr = '00:21:11:01:FA:1C'
buf_size = 1024


s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
port = 1
s.connect((adapter_addr, port))
while True:
    x = input("command: ")
    s.send(x.encode())


