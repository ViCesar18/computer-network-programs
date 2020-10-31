import socket

""" sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8888))
sock.settimeout(None)

try:
    sock.recvfrom(1024)
except socket.timeout:
    print('Nao recebeu nenhum pacote!') """

HEADER_SIZE = 8
package_id = 987421

header = bytes('{:0>8}'.format(format(package_id, 'X')), 'utf-8')      #Faz um header com caracteres com um identificador único para cada pacote, em hexadecimal
package_id += 1
package = b''.join([header, b'eae'])

package_id = int(str(package)[2:HEADER_SIZE+2], 16)

print(package_id)
print(package[HEADER_SIZE:])
