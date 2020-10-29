import socket
import time

ip = '0.0.0.0'
port = 8888

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((ip, port))

PACKAGE_SIZE = 1024
TRANSMISSION_WINDOW = 4
HEADER_SIZE = 16
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

transmission_start = time.time()

data, client_addr = server_socket.recvfrom(PACKAGE_SIZE)
file_name = data.decode()

data, client_addr = server_socket.recvfrom(PACKAGE_SIZE)
FILE_SIZE = int(data.decode())

data, client_addr = server_socket.recvfrom(PACKAGE_SIZE)
TOTAL_PACKAGES = int(data.decode())

package_list = {}

f = open(f'./baixado/{file_name}', 'wb')

total_packages_counter = 0
while True:
    counter = 0

    while counter < TRANSMISSION_WINDOW:
        data, client_addr = server_socket.recvfrom(PACKAGE_SIZE)
        print(f'Recebendo pacote {total_packages_counter + counter + 1}')

        if '0000000000000000' in str(data)[:16]:
            print('Pacote nulo recebido.')
            break

        index = int(str(data)[2:HEADER_SIZE+2], 16)
        package_list[index] = data[HEADER_SIZE:]

        counter = counter + 1

    if '0000000000000000' in str(data)[:16]:
        print('Pacote nulo recebido.')
        break
    
    window_package_counter = index - TRANSMISSION_WINDOW + 1
    
    while True:
        f.write(package_list[window_package_counter])
        window_package_counter = window_package_counter + 1

        if(window_package_counter == index + 1):
            package_list.clear()
            break
    
    server_socket.sendto(b'RECEIVED!', client_addr)

    total_packages_counter = total_packages_counter + TRANSMISSION_WINDOW
    if total_packages_counter >= TOTAL_PACKAGES:
        break


f.close()
server_socket.close()

transmission_end = time.time()
transmission_time = transmission_end - transmission_start

print('\nArquivo enviado com sucesso!')
print(f'Tamanho do arquivo: {FILE_SIZE / 1024} kB')
print(f'Número de Pacotes transmitidos: {TOTAL_PACKAGES}')
print(f'Tamanho dos Pacotes: {PACKAGE_SIZE}')
print(f'Tamanho da Janela de Transmissao: {TRANSMISSION_WINDOW}')
print(f'Velocidade de Transmissão: {round((TOTAL_PACKAGES * PACKAGE_SIZE * 8) / 1024 / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits
