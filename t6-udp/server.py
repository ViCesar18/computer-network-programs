import socket

ip = '0.0.0.0'
port = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, port))

addr = (ip, port)
package_size = 1024
buffer_size = 8
buffer = []
i = 0

f = open('./recebido/uel.jpg', 'wb')

package_number = 0

Count, countadress = server_socket.recvfrom(package_size)

tillI = Count.decode()
tillI = int(tillI)

while True:
    package, addr = server_socket.recvfrom(package_size)

    if package == b'OK!':
        print('porra')
        for data in buffer:
            f.write(data)

        buffer = []
    elif package == b'QNTD?':
        server_socket.sendto(str(i).encode(), addr)
        i = 0
    elif package == b'RES!':
        buffer = []
    else:
        buffer.append(package)
        
        i += 1
        package_number += 1
        tillI -= 1  
        print(f"Recebendo pacote numero: {package_number}")

f.close()
server_socket.close()