import datetime
import socket

## DOWNLOAD

HOST = '0.0.0.0'
PORT = 8888
BUFFER = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(0)
print(f'\nEscutando em {HOST}:{PORT}\n')

client_sock, client_addr = sock.accept()

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} conectado\n')

count = 0
print_count = 1

print('### Testando Download ###')
while True:
    data = client_sock.recv(BUFFER)

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
    client_sock.close()

    endtime = datetime.datetime.now()
    print(endtime, end=' ')
    print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')

    print('## RESULTADO ##')
    print(f'Bytes transferidos: {count / 1024 / 1024} MB')
    delta = endtime - starttime
    print(f'Tempo usado (segundos): {delta.seconds}')
    speed = (count * 8) / 1024 / 1024 / delta.seconds
    print(f'Velocidade Média (Mbps): {speed}\n')
    break

## UPLOAD

sock.listen(0)
print(f'Escutando em {HOST}:{PORT}\n')

client_sock, client_addr = sock.accept()

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} conectado\n')

count = 0
print_count = 1

print('### Testando Upload ###')

testdata = b'x' * BUFFER * 4

while True:
    client_sock.send(testdata)
    count += len(testdata)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= print_count):
        print_count = print_count + 1
        print('.', end='', flush=True)

    if(delta.seconds >= 20):
        client_sock.close()
        break

print('\n')
sock.close()

endtime = datetime.datetime.now()
print(endtime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')

print('## RESULTADO ##')
print(f'Bytes transferidos: {count / 1024 / 1024} MB')
delta = endtime - starttime
print(f'Tempo usado (segundos): {delta.seconds}')
speed = (count * 8) / 1024 / 1024 / delta.seconds
print(f'Velocidade Média (Mbps): {speed}\n')
