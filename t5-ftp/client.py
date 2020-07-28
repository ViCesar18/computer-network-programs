import socket
import time

IP = '192.168.0.106'
PORT = 8888

#IP = input('IP: ')
#PORT = int(input('Porta: '))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Cria o socket do cliente
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Ajusta o socket para permitir reconexão no mesmo (IP, PORT)
client_socket.connect((IP, PORT))   #Faz a conexão com o servidor

f = open('./enviado/file.txt', 'rb')

package_size = 1024
package_number = 0
package = f.read(package_size)

transmission_start = time.time()
while package:
	package_number += 1
	print(f'Enviando pacote {package_number}')
	client_socket.send(package)
	package = f.read(package_size)

transmission_end = time.time()
transmission_time = transmission_end - transmission_start

f.close()
print('\nArquivo enviado com sucesso!')
print(f'Tamanho do arquivo: {package_number * package_size} Bytes')
print(f'Número de Pacotes transmitidos: {package_number}')
print(f'Velocidade de Transmissão: {round((package_number * package_size * 8) / 1024 / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits

client_socket.shutdown(socket.SHUT_WR)
client_socket.close()
