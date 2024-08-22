import threading
import socket

#Host e porta para o servidor
host = '127.0.0.1'  #local
porta = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, porta))
server.listen()

#Cada novo usuário é um novo objeto na lista de usuários
usuarios = []
nicks = []


#Função para enviar mensagens para todos os usuários
def transmissao(mensagem):
    for usuario in usuarios:
        usuario.send(mensagem)

#Função para lidar com as mensagens dos usuários
def handle(usuario):
    while True:
        try:
            mensagem = usuario.recv(1024)
            transmissao(mensagem)
        except:
            index = usuarios.index(usuario)
            usuarios.remove(usuario)
            usuario.close()
            nick = nicks[index]
            transmissao(f'{nick} saiu do chat!'.encode('ascii'))
            nicks.remove(nick)
            break

#Função para receber conexões
def receber_conexao():
    while True:
        usuario, endereco = server.accept()
        print(f"Conectado com {str(endereco)}")

        usuario.send('NICK'.encode('ascii'))
        nick = usuario.recv(1024).decode('ascii')
        nicks.append(nick)
        usuarios.append(usuario)

        print(f"O nick do usuário é {nick}!")
        transmissao(f"{nick} entrou no chat!\n".encode('ascii'))
        usuario.send('Conectado ao servidor!\n'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(usuario,))
        thread.start()


print("Servidor está online")
receber_conexao()