import socket

ip = '0.0.0.0'
port = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, port))

addr = (ip, port)
buffer = 1024

f = open('./recebido/img.jpg', 'wb')

package_number = 0

Count, countadress = server_socket.recvfrom(buffer)

tillI = Count.decode('utf-8')
tillI = int(tillI)

while tillI != 0:
    data, addr = server_socket.recvfrom(buffer)
    f.write(data)
    
    package_number += 1
    tillI -= 1
    print(f"Recebendo pacote numero: {package_number}")

f.close()
server_socket.close()