import datetime
import socket

## DOWNLOAD DO CLIENTE

HOST = '0.0.0.0'
PORT = 8888
PACKAGE_SIZE = 4096

HEADER_SIZE = 8
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

print(f'\nVinculado em {HOST}:{PORT}\n')

data, client_addr = sock.recvfrom(PACKAGE_SIZE)
if data == b'CONNECT!':
    sock.sendto(b'CONNECTED', client_addr)
else:
    print('Server nao se conectou com o cliente!')
    exit(1)

print("### Testando Download do Cliente ###\n")

sock.settimeout(3)

starttime = datetime.datetime.now()
package_id = 1
count_timeout = 0
packages_resent = 0
payload = b'x' * PAYLOAD_SIZE

while True:
    header = bytes('{:0>8}'.format(format(package_id, 'X')), 'utf-8')      #Faz um header com caracteres com um identificador único para cada pacote, em hexadecimal
    package_id += 1
    package = b''.join([header, payload])

    while True:     #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo
        try:
            sock.sendto(package, client_addr)
            data, client_addr = sock.recvfrom(PACKAGE_SIZE)

            if(data == b'OK!'):
                break
        except socket.timeout:
            packages_resent = packages_resent + 1
            continue

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= 20):
        header = bytes('{:0>8}'.format(0), 'utf-8')      #Faz um header com HEADER_SIZE 0's, em hexadecimal
        package = b''.join([header, b'END!'])

        while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
            try:
                sock.sendto(package, client_addr)
                data, client_addr = sock.recvfrom(PACKAGE_SIZE)

                if data == b'OK!':
                    break
            except socket.timeout:
                if count_timeout == 5:
                    break
                else:
                    count_timeout = count_timeout + 1
                    continue
        break

count_timeout = 0
while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até um máximo de 5 vezes
    try:
        sock.sendto(str(packages_resent).encode(), client_addr)
        data, client_addr = sock.recvfrom(PACKAGE_SIZE)

        if data == b'OK!':
            break
    except socket.timeout:
        if count_timeout == 5:
            break
        else:
            count_timeout = count_timeout + 1
            continue

## UPLOAD DO CLIENTE
print("### Testando Upload do Cliente ###\n")

sock.settimeout(None)

print_count = 1
package_list = {}
duplicate_packages = 0

while True:
    package, server_socket = sock.recvfrom(PACKAGE_SIZE)

    package_id = int(str(package)[2:HEADER_SIZE+2], 16)
    if not package_list.get(package_id):
        package_list[package_id] = package[HEADER_SIZE:]
    else:
        duplicate_packages = duplicate_packages + 1

    sock.sendto(b'OK!', client_addr)

    if package_id != 0:
        continue

    package_list.clear()

    break

sock.settimeout(3)

while True: #Caso o não receba a comfirmação em um determinado tempo, envia o pacote de novo, até perder a conexão com o cliente
    try:
        sock.sendto(str(duplicate_packages).encode(), client_addr)
        data, client_addr = sock.recvfrom(PACKAGE_SIZE)

        if data == b'OK!':
            break
    except socket.timeout:
        continue
    except ConnectionResetError:
        break

sock.close()
