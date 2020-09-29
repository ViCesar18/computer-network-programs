import socket
import os

ip = '192.168.0.104'
port = 8888

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

package_size = 1024
buffer = []
buffer_size = 8
addr = (ip, port)

size = os.stat('./enviado/uel.jpg')
sizeS = size.st_size   #número de pacotes
Num = int(sizeS / package_size)
Num = Num + 1
print(f"Número de Pacotes para ser enviado: {str(Num)}")

till = str(Num)
tillC = till.encode()
client_socket.sendto(tillC, addr)

tillIC = int(Num)

f = open('./enviado/uel.jpg', 'rb')

package_number = 0

while tillIC != 0:
    package = f.read(package_size)
    client_socket.sendto(package, addr)
    buffer.append(package)

    package_number += 1
    tillIC -= 1
    print(f'Enviando pacote numero: {package_number}')

    if len(buffer) == buffer_size or tillIC == 0:
        if tillIC == 0:
            buffer_size = len(buffer)
        
        client_socket.sendto(b'QNTD?', addr)

        pacotes_recebidos_pelo_servidor, _ = client_socket.recvfrom(package_size)

        pacotes_recebidos_pelo_servidor = int(pacotes_recebidos_pelo_servidor.decode('utf-8'))
        i = package_number - buffer_size
        
        while pacotes_recebidos_pelo_servidor != buffer_size:
            client_socket.sendto(b'RES!', addr)
            for data in buffer:
                print(f'Reenviando pacote numero: {i}')
                client_socket.sendto(data, addr)
                i += 1
            
            client_socket.sendto(b'QNTD?', addr)
            pacotes_recebidos_pelo_servidor = client_socket.recvfrom(package_size)
            i = package_number - buffer_size

        buffer = []
        client_socket.sendto(b'OK!', addr)
        print('porra')
    
f.close()
client_socket.close()
