import sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread



def verifica_ip(endereco_ip):
    if len(endereco_ip) == 9 and endereco_ip is not None:
        return True
    print("Ip imcompativel, encerrando programa")
    sys.exit()



def chat():
    mensagem = input()
    if mensagem is not None:
        con_tcp.send(bytes(mensagem, "utf8"))



def chatrecebe():
        while True:
            try:
                recv_mens = con_tcp.recv(1024).decode("utf8") 
                if recv_mens is not None:
                    print(recv_mens)
            except OSError:
                 break

            

SERVER_PORT = 8001

print("Bem vindo ao Chat sem nome no momento!\n")
ip = input("Entre com o endereço de ip desejado para começar a se comunicar \n")

print("Tentando conectar ao servidor")
if verifica_ip(ip):
    print("ip valido!")
ADDR = (ip, SERVER_PORT)
con_tcp = socket(AF_INET,SOCK_STREAM)
con_tcp.connect(ADDR)
print("Chat iniciado! Para sair escreva: exit ")
print("Escreva seu nome: ")
while True:
    chat()
    receive_thread = Thread(target=chatrecebe)
    receive_thread.start()
