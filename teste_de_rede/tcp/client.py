import datetime
import socket

## DOWNLOAD DO SERVIDOR

HOST = input('Digite o IP que deseja conectar: ')
PORT = 8888
BUFFER = 4096

testdata = b'x' * BUFFER * 4

print("\n### Testando Download do Servidor ###")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'Conectado à {HOST}:{PORT}\n')

while True:
    sock.send(testdata)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= 20):
        break

sock.close()

endtime = datetime.datetime.now()
print(endtime, end=' ')
print(f'Desconectado de {HOST}:{PORT}\n')

## UPLOAD DO SERVIDOR

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'Conectado à {HOST}:{PORT}\n')

count = 0

print("### Testando Upload do Servidor ###")
while True:
    data = sock.recv(BUFFER)
    if data:
        count += len(data)
        del data
        continue

    sock.close()

    endtime = datetime.datetime.now()
    print(endtime, end=' ')
    print(f'Desconectado de {HOST}:{PORT}\n')

    break

sock.close()
