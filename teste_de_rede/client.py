import socket
import os
import time

ip = '201.21.146.35'
port = 8888

ip = input('IP: ')
port = int(input('PORT: '))
file_name = input('Nome do Arquivo: ')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

package_size = 1024
addr = (ip, port)

client_socket.sendto(file_name.encode(), addr)  #Envia o nome do arquivo

size = os.stat(file_name)
sizeS = size.st_size   #número de pacotes
Num = int(sizeS / package_size)
Num = Num + 1
print(f"Número de Pacotes para ser enviado: {str(Num)}")

till = str(Num)
tillC = till.encode()
client_socket.sendto(tillC, addr)

tillIC = int(Num)

f = open(file_name, 'rb')

package_number = 0

transmission_start = time.time()
while tillIC != 0:
    package = f.read(package_size)
    client_socket.sendto(package, addr)

    package_number += 1
    tillIC -= 1

    print(f"Pacote numero {package_number} enviado!")
    
    while True:
        server_package, server_addr = client_socket.recvfrom(package_size)

        if(server_package == b'RECEIVED!'):
            break

        client_socket.sendto(package, addr)
        print(f"Pacote numero {package_number} reenviado!")

client_socket.sendto(b'END!', addr)
    
f.close()
client_socket.close()

transmission_end = time.time()
transmission_time = transmission_end - transmission_start

print('\nArquivo enviado com sucesso!')
print(f'Tamanho do arquivo: {package_number * package_size} Bytes')
print(f'Número de Pacotes transmitidos: {package_number}')
print(f'Tamanho dos Pacotes: {package_size}')
print(f'Velocidade de Transmissão: {round((package_number * package_size * 8) / 1024 / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits
