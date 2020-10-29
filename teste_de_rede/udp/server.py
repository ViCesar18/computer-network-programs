import datetime
import socket

## DOWNLOAD DO CLIENTE

HOST = '0.0.0.0'
PORT = 8888
PACKAGE_SIZE = 4096

HEADER_SIZE = 16
PAYLOAD_SIZE = PACKAGE_SIZE - HEADER_SIZE

testdata = b'x' * PAYLOAD_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST,PORT))

print(f'\nVinculado em {HOST}:{PORT}\n')

print("### Testando Download do Cliente ###\n")

data, client_addr = sock.recvfrom(PACKAGE_SIZE)
if data != b'OK!':
    print('Nao se conectou com o cliente!')
    exit(1)

starttime = datetime.datetime.now()

while True:
    sock.sendto(testdata, client_addr)

    endtime = datetime.datetime.now()
    delta = endtime - starttime

    if(delta.seconds >= 20):
        sock.sendto(b'END!', client_addr)
        break

endtime = datetime.datetime.now()

## UPLOAD DO CLIENTE
print("### Testando Upload do Cliente ###\n")

starttime = datetime.datetime.now()
package_lost = 0
package_controll = []

while True:
    data, client_addr = sock.recvfrom(PACKAGE_SIZE)
    if data != b'END!':
        index = int(str(data)[2:HEADER_SIZE+2], 16)
        package_controll.append(index)

        del data
        continue

    endtime = datetime.datetime.now()

    break

package_controll.sort()
counter = 1
for i in package_controll:
    if(i != counter):
        package_lost = package_lost + 1
    
    counter = counter + 1

sock.sendto(str(package_lost).encode(), client_addr)

sock.close()
