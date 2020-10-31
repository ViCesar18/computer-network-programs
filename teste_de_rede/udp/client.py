import datetime
import socket

## DOWNLOAD

HOST = input('Digite o IP que deseja conectar: ')
PORT = 8888
PACKAGE_SIZE = 4096
ADDR = (HOST, PORT)

HEADER_SIZE = 8
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

print(f'\nTamanho do HEADER: {HEADER_SIZE}')
print(f'Tamanho do PAYLOAD: {PAYLOAD_SIZE}\n')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(3)

while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo
    try:
        sock.sendto(b'CONNECT!', ADDR)
        data, server_addr = sock.recvfrom(PACKAGE_SIZE)

        if data:
            break
    except socket.timeout:
        continue

sock.settimeout(None)

starttime = datetime.datetime.now()
package_id = 1
package_counter = 0
print_count = 1
duplicated_packages = 0
package_list = {}

print('### Testando Download ###')
while True:
    package, server_socket = sock.recvfrom(PACKAGE_SIZE)

    package_counter = package_counter + 1

    package_id = int(str(package)[2:HEADER_SIZE+2], 16)
    if not package_list.get(package_id):
        package_list[package_id] = package[HEADER_SIZE:]
    else:
        duplicated_packages = duplicated_packages + 1

    sock.sendto(b'OK!', ADDR)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if package_id != 0:
        if(delta.seconds >= print_count):
            print_count = print_count + 1
            print('.', end='', flush=True)

        continue

    package_list.clear()

    data, server_addr = sock.recvfrom(PACKAGE_SIZE)
    sock.sendto(b'OK!', ADDR)

    packages_resent = int(data.decode())

    packages_lost = packages_resent - duplicated_packages
    bytes_transferred = package_counter * PACKAGE_SIZE / 1024 / 1024
    delta = endtime - starttime
    speed = round(bytes_transferred * 8 / delta.seconds, 2)

    print('\n## RESULTADO ##')
    print(f'Pacotes Recebidos: {package_counter}')
    print(f'Pacotes Perdidos: {packages_lost}')
    print(f'Bytes Transferidos: {round(bytes_transferred, 2)} MB')
    print(f'Velocidade Média: {speed} Mbps')
    print(f'Tempo: {delta.seconds} segundos\n')
    break

## UPLOAD

sock.settimeout(3)

starttime = datetime.datetime.now()
package_id = 1
package_counter = 0
count_timeout = 0
print_count = 1
packages_resent = 0
payload = b'x' * PAYLOAD_SIZE

print('\n### Testando Download ###')
while True:
    header = bytes('{:0>8}'.format(format(package_id, 'X')), 'utf-8')      #Faz um header com caracteres com um identificador único para cada pacote, em hexadecimal
    package_id += 1
    package = b''.join([header, payload])

    package_counter = package_counter + 1
    while True:     #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo
        try:
            sock.sendto(package, ADDR)
            data, server_addr = sock.recvfrom(PACKAGE_SIZE)

            if(data == b'OK!'):
                break
        except socket.timeout:
            packages_resent = packages_resent + 1
            continue

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= print_count):
        print_count = print_count + 1
        print('.', end='', flush=True)

    if(delta.seconds >= 20):
        header = bytes('{:0>8}'.format(0), 'utf-8')      #Faz um header com HEADER_SIZE 0's, em hexadecimal
        package = b''.join([header, b'END!'])

        while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
            try:
                sock.sendto(package, ADDR)
                data, server_socket = sock.recvfrom(PACKAGE_SIZE)

                if data == b'OK!':
                    break
            except socket.timeout:
                if count_timeout == 5:
                    break
                else:
                    count_timeout = count_timeout + 1
                    continue
        break

sock.settimeout(None)

data, server_addr = sock.recvfrom(PACKAGE_SIZE)
sock.sendto(b'OK!', ADDR)

duplicated_packages = int(data.decode())

sock.close()

packages_lost = packages_resent - duplicated_packages
bytes_transferred = package_counter * PACKAGE_SIZE / 1024 / 1024
delta = endtime - starttime
speed = round(bytes_transferred * 8 / delta.seconds, 2)

print('\n\n## RESULTADO ##')
print(f'Pacotes Enviados: {package_counter}')
print(f'Pacotes Perdidos: {packages_lost}')
print(f'Bytes Transferidos: {round(bytes_transferred, 2)} MB')
print(f'Velocidade Média: {speed} Mbps')
print(f'Tempo: {delta.seconds} segundos\n')
