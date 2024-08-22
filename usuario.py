import socket
import threading

usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
usuario.connect(('127.0.0.1', 55555))

nick = input("Escolha um nick: ")
usuario.send(nick.encode('ascii'))

def receber_mensagem():
    while True:
        try:
            mensagem = usuario.recv(1024).decode('ascii')
            if mensagem == 'NICK':
                usuario.send(nick.encode('ascii'))
            else:
                print(mensagem)
        except:
            print("Um erro ocorreu!")
            usuario.close()
            break

def escrever_mensagem():
    while True:
        mensagem = f'{nick}: {input("")}'
        usuario.send(mensagem.encode('ascii'))

thread_receber = threading.Thread(target=receber_mensagem)
thread_receber.start()

thread_escrever = threading.Thread(target=escrever_mensagem)
thread_escrever.start()
