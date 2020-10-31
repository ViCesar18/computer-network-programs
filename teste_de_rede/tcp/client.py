import datetime
import socket

## DOWNLOAD

HOST = input('Digite o IP que deseja conectar: ')
PORT = 8888
BUFFER = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

starttime = datetime.datetime.now()
""" print(starttime, end=' ')
print(f'Conectado à {HOST}:{PORT}\n') """

count = 0
print_count = 1

print('\n### Testando Download ###')
while True:
    data = sock.recv(BUFFER)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if data:
        count += len(data)
        del data

        if(delta.seconds >= print_count):
            print_count = print_count + 1
            print('.', end='', flush=True)

        continue
    
    print('\n')
    sock.close()

    endtime = datetime.datetime.now()
    """ print(endtime, end=' ')
    print(f'Desconectado de {HOST}:{PORT}\n') """

    print('## RESULTADO ##')
    print(f'Bytes Transferidos: {count / 1024 / 1024} MB')
    delta = endtime - starttime
    print(f'Tempo (segundos): {delta.seconds}')
    speed = (count * 8) / 1024 / 1024 / delta.seconds
    print(f'Velocidade Média (Mbps): {speed}\n')
    break

## UPLOAD

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

starttime = datetime.datetime.now()
""" print(starttime, end=' ')
print(f'Conectado à {HOST}:{PORT}\n') """

count = 0
print_count = 1

print('### Testando Upload ###')

testdata = b'x' * BUFFER * 4

while True:
    sock.send(testdata)
    count += len(testdata)

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
""" print(endtime, end=' ')
print(f'Desconectado de {HOST}:{PORT}\n') """

print('## RESULTADO ##')
print(f'Bytes Transferidos: {count / 1024 / 1024} MB')
delta = endtime - starttime
print(f'Tempo (segundos): {delta.seconds}')
speed = (count * 8) / 1024 / 1024 / delta.seconds
print(f'Velocidade Média (Mbps): {speed}\n')
