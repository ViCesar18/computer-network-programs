import datetime
import socket

## DOWNLOAD DO SERVIDOR

HOST = '127.0.0.1'
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

    if(delta.seconds >= 5):
        break

sock.close()

endtime = datetime.datetime.now()
print(endtime, end=' ')
print(f'Desconectado de {HOST}:{PORT}\n')

## UPLOAD DO SERVIDOR

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST,PORT))
sock.listen(0)
print(f'Escutando em {HOST}:{PORT}\n')

client_sock, client_addr = sock.accept()

starttime = datetime.datetime.now()
print(starttime, end=' ')
print(f'{client_addr[0]}:{client_addr[1]} conectado\n')

count = 0

print("### Testando Upload do Servidor ###")
while True:
    data = client_sock.recv(BUFFER)
    if data:
        count += len(data)
        del data
        continue

    client_sock.close()

    endtime = datetime.datetime.now()
    print(endtime, end=' ')
    print(f'{client_addr[0]}:{client_addr[1]} desconectado\n')

    break

sock.close()
