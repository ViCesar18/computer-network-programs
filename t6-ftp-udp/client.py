import socket
import os
import time
import math

""" ip = '201.21.146.35'
port = 8888 """

ip = input('IP: ')
port = 8888
file_name = input('Nome do Arquivo: ')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
f = open(file_name, 'rb')

ADDR = (ip, port)
PACKAGE_SIZE = 1024
TRANSMISSION_WINDOW = 4
HEADER_SIZE = 16
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

f.seek(0, 2)
FILE_SIZE = f.tell()
f.seek(0)

TOTAL_PACKAGES = math.ceil(FILE_SIZE / PAYLOAD_SIZE)

package_counter = 1

transmission_start = time.time()

client_socket.sendto(file_name.encode(), ADDR)  #Envia o nome do arquivo

client_socket.sendto(str(FILE_SIZE).encode(), ADDR) #Envia o tamanho do arquivo

client_socket.sendto(str(TOTAL_PACKAGES).encode(), ADDR)    #Envia o número total de pacotes

while package_counter - 1 < TOTAL_PACKAGES:
    for i in range(TRANSMISSION_WINDOW):
        payload = f.read(PAYLOAD_SIZE)
        header = bytes('{:0>16}'.format(format(package_counter, 'X')), 'utf-8')      #Faz um header com caracteres com o contador de pacotes em hexadecimal
        package = b''.join([header, payload])

        client_socket.sendto(package, ADDR)
        print(f'Enviando pacote {package_counter}')

        package_counter += 1

    client_socket.recvfrom(PACKAGE_SIZE)

client_socket.sendto(b'END!', ADDR)

f.close()
client_socket.close()

transmission_end = time.time()
transmission_time = transmission_end - transmission_start

print('\nArquivo enviado com sucesso!')
print(f'Tamanho do arquivo: {FILE_SIZE / 1024} kB')
print(f'Número de Pacotes transmitidos: {TOTAL_PACKAGES}')
print(f'Tamanho dos Pacotes: {PACKAGE_SIZE}')
print(f'Tamanho da Janela de Transmissao: {TRANSMISSION_WINDOW}')
print(f'Velocidade de Transmissão: {round((TOTAL_PACKAGES * PACKAGE_SIZE * 8) / 1024 / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits
