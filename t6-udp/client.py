import socket
import os

ip = '192.168.0.107'
port = 8888

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

buffer = 1024
addr = (ip, port)

size = os.stat('./enviado/img.jpg')
sizeS = size.st_size   #número de pacotes
Num = int(sizeS / buffer)
Num = Num + 1
print(f"Número de Pacotes para ser enviado: {str(Num)}")

till = str(Num)
tillC = till.encode('utf-8')
client_socket.sendto(tillC, addr)

tillIC = int(Num);

f = open('./enviado/img.jpg', 'rb')

package_number = 0

while tillIC != 0:
    package = f.read(buffer)
    client_socket.sendto(package, addr)
    package_number += 1
    tillIC -= 1
    print(f'Enviando pacote numero: {package_number}')
    
f.close()
client_socket.close()
