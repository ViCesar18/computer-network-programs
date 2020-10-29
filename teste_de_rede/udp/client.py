import datetime
import socket

## DOWNLOAD

HOST = input('Digite o IP que deseja conectar: ')
PORT = 8888
PACKAGE_SIZE = 4096
ADDR = (HOST, PORT)

HEADER_SIZE = 16
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto(b'OK!', ADDR)

starttime = datetime.datetime.now()

count = 0
print_count = 1

print('\n### Testando Download ###')
while True:
    data, server_socket = sock.recvfrom(PACKAGE_SIZE)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if data != b'END!':
        count += len(data)
        del data

        if(delta.seconds >= print_count):
            print_count = print_count + 1
            print('.', end='', flush=True)

        continue
    
    print('\n')

    endtime = datetime.datetime.now()

    print('## RESULTADO ##')
    print(f'Bytes Transferidos: {round(count / 1024 / 1024, 2)} MB')
    delta = endtime - starttime
    print(f'Tempo (segundos): {delta.seconds}')
    speed = int((count * 8) / 1024 / 1024 / delta.seconds)
    print(f'Velocidade Média (Mbps): {speed}\n')
    break

## UPLOAD DO SERVIDOR

starttime = datetime.datetime.now()

count = 0
print_count = 1

print('### Testando Upload ###')

payload = b'x' * PAYLOAD_SIZE
header_count = 1

while True:
    header = bytes('{:0>16}'.format(format(header_count, 'X')), 'utf-8')      #Faz um header com caracteres com o contador de pacotes em hexadecimal
    header_count += 1
    package = b''.join([header, payload])
    sock.sendto(package, ADDR)
    count += len(package)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= print_count):
        print_count = print_count + 1
        print('.', end='', flush=True)

    if(delta.seconds >= 20):
        sock.sendto(b'END!', ADDR)
        break

print('\n')

endtime = datetime.datetime.now()

data, server_addr = sock.recvfrom(PACKAGE_SIZE)
package_lost = data.decode()

sock.close()

print('## RESULTADO ##')
print(f'Bytes Transferidos: {round(count / 1024 / 1024, 2)} MB')
print(f'Pacotes Perdidos: {package_lost}')
delta = endtime - starttime
print(f'Tempo (segundos): {delta.seconds}')
speed = int((count * 8) / 1024 / 1024 / delta.seconds)
print(f'Velocidade Média (Mbps): {speed}\n')
