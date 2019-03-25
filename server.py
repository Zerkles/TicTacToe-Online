import socket

BUFFER_SIZE = 20  # Normally 1024, but we want fast response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 2137))
server_socket.listen(1)

client_socket, addr = server_socket.accept()
print('Connection address:', addr)

while 1:
  data = client_socket.recv(1024)
  if not data: break
  print("received data:", data.decode())
  client_socket.send(data)  # echo

client_socket.close()