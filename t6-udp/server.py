from socket import *

ip = '0.0.0.0'
port = 8888

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((ip, port))

addr = (ip, port)
buffer = 1024

f = open('./recebido/img.jpg', 'wb')


package, addr = server_socket.recvfrom(buffer)
try:
    while package:
        f.write(package)
        server_socket.settimeout(2)
        data, addr = server_socket.recvfrom(buffer)
except timeout:
    f.close()
    server_socket.close()
    print('Arquivo Baixado')