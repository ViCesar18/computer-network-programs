import datetime
import socket

## DOWNLOAD

HOST = input('Digite o IP que deseja conectar: ')
PORT = 8888
PACKAGE_SIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

starttime = datetime.datetime.now()
package_count = 0
print_count = 1

print('\n### Testando Download ###')
while True:
    data = sock.recv(PACKAGE_SIZE)
    package_count = package_count + 1

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if data:
        del data

        if(delta.seconds >= print_count):
            print_count = print_count + 1
            print('.', end='', flush=True)

        continue
    
    print('\n')
    sock.close()

    endtime = datetime.datetime.now()
    delta = endtime - starttime
    bytes_transferred = round(package_count * PACKAGE_SIZE / 1024 / 1024, 2)
    speed = round(bytes_transferred * 8 / delta.seconds, 2)

    print('## RESULTADO ##')
    print(f'Pacotes Recebidos: {package_count}')
    print(f'Bytes Transferidos: {bytes_transferred} MB')
    print(f'Velocidade Média: {speed} Mbps')
    print(f'Tempo: {delta.seconds} segundos\n')
    break

## UPLOAD

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

starttime = datetime.datetime.now()

package_count = 0
print_count = 1
package = b'x' * PACKAGE_SIZE * 4

print('### Testando Upload ###')
while True:
    sock.send(package)
    package_count = package_count + 1

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= print_count):
        print_count = print_count + 1
        print('.', end='', flush=True)

    if(delta.seconds >= 20):
        break

print('\n')
sock.close()

endtime = datetime.datetime.now()
delta = endtime - starttime
bytes_transferred = round(package_count * PACKAGE_SIZE / 1024 / 1024, 2)
speed = round(bytes_transferred * 8 / delta.seconds, 2)

print('## RESULTADO ##')
print(f'Pacotes Enviados: {package_count}')
print(f'Bytes Transferidos: {bytes_transferred} MB')
print(f'Velocidade Média: {speed} Mbps')
print(f'Tempo: {delta.seconds} segundos\n')
