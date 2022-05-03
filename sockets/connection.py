# import socket

# adapter_addr = '00:21:11:01:FA:1C'
# port = 1  # Normal port for rfcomm?
# buf_size = 1024

# s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
# s.bind((adapter_addr, port))
# s.listen(1)
# try:
#     print('Listening for connection...')
#     client, address = s.accept()
#     print(f'Connected to {address}')

#     while True:
#         data = client.recv(buf_size)
#         if data:
#             print(data)
# except Exception as e:
#     print(f'Something went wrong: {e}')
#     client.close()
#     s.close()

import bluetooth 

hostMACAddress = '' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters. 
port = 1
backlog = 1
size = 1024

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
try:
	client, clientInfo = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data) # Echo back to client
except:	
	print("Closing socket")
	client.close()
	s.close()