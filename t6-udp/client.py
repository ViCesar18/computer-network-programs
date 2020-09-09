from socket import *

ip = '192.168.0.107'
port = 8888

client_socket = socket(AF_INET, SOCK_DGRAM)

buffer = 1024
addr = (ip, port)

f = open('./enviado/img.jpg', 'rb')

package_number = 0
package = f.read(buffer)

while package:
    if(client_socket.sendto(package, addr)):
        package_number += 1
        print(f'Enviando pacote {package_number}')
        package = f.read(buffer)

client_socket.close()
f.close()