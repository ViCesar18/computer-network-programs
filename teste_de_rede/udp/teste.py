arquivo = open('uel.jpg', 'rb')

contador_pacotes = 17

bytes_lidos = arquivo.read(1024 - 16)

message_contador = bytes('{:0>16}'.format(format(contador_pacotes, 'x')), 'utf8')

message = b"".join([message_contador, b'eae'])

lista = {}
lista['a'] = 2

print(lista)

""" sock.sendto(message, server_address)

contador_pacotes += 1 """