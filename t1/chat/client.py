import socket
import errno
import sys
from threading import Thread

IP = input("IP: ")
PORT = int(input("Port: "))
my_username = input("Usuário: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Ajusta o socket para permitir reconexão no mesmo (IP, PORT)
client_socket.connect((IP, PORT))

username = my_username.encode("utf-8")
client_socket.send(username)


def receberMensagens(): #Recebe as mensagens enviadas por todos os outros clientes conectados ao servidor
    try:
        while True:
                message = client_socket.recv(2048).decode("utf-8")

                print(f"{message}")
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading Error', str(e))
            sys.exit()
        return

    except Exception as e:
        print('Gereral Error', str(e))
        sys.exit()


while True:
    processo = Thread(target = receberMensagens)    #Processo paralelo que permite o recebimento de mensagens
    processo.start()                                #por mais que o processo principal esteja aguardando o input

    message = input()   #Envia uma mensagem para o servidor distribuir

    if message:
        message = message.encode("utf-8")
        client_socket.send(message)

