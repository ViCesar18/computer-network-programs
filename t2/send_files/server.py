import socket
import time

IP = '192.168.0.106'
PORT = 8888

#IP = input('IP: ')
#PORT = int(input('Porta: '))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Cria o socket do servidor
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     #Ajusta o socket para permitir reconexão no mesmo (IP, PORT)

server_socket.bind((IP, PORT))

f = open('./recebido/file.txt', 'wb')

server_socket.listen()

while True:
	client_socket, addr = server_socket.accept()
	print(f'Conexão estabelecida de ({addr})')

	package_size = 1024
	package_number = 0
	package = client_socket.recv(package_size)

	transmission_start = time.time()
	while package:
		package_number += 1
		print(f'Recebendo pacote {package_number}')
		f.write(package)
		package = client_socket.recv(package_size)

	transmission_end = time.time()
	transmission_time = transmission_end - transmission_start

	f.close()
	print('\nArquivo recebido com sucesso!')
	print(f'Tamanho do arquivo: {package_number * package_size} Bytes')
	print(f'Número de Pacotes recebidos: {package_number}')
	print(f'Velocidade de Transmissão: {round((package_number * package_size * 8) / 1024 / transmission_time, 2)} kb/s') #Multiplicado por 8 para converter Bytes para Bits

	client_socket.close()