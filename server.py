from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, gethostname
from threading import Thread




def accept_conexoes():
    while True:
        client, client_address = SERVER.accept()
        enderecos[client] = client_address
        Thread(target=trata_client, args=(client,)).start()


def trata_client(client):
    name = client.recv(650724).decode("utf8")
    client.send(bytes(name + " está online!", "utf8"))
    msg = "%s entrou no chat!" % name
    broadcast(bytes(msg, "utf8"))
    print(name, " - ENTROU NO SERVER")
    clients[client] = name

    while True:
        msg = client.recv(650724) 
        if msg != bytes("exit", "utf8"):
            if msg.startswith(b"IMAGE:"):
                
                broadcastimg(msg)
                #broadcast(b"", name + " enviou uma imagem.")
                print(name, " - enviou uma imagem")
                return
            else:
                broadcast(msg, name + ": ")
                print(name, " - mandou a seguinte msg: ", msg)
        else:   
            client.send(bytes("exit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s saiu do chat" % name, "utf8"))
            print(name, " - SAIU DO SERVER")
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def broadcastimg(msg):
    for sock in clients:
        print("Server msg len", len(msg))
        sock.send(msg)

        


clients = {}
enderecos = {}

SERVER_PORT = 9050
HOST = gethostbyname(gethostname())
print("host: ", HOST)
ADDR = (HOST, SERVER_PORT)

SERVER = socket(AF_INET, SOCK_STREAM)

SERVER.bind(ADDR)

SERVER.listen(5)
print("Aguardando conexão...")
ACCEPT_THREAD = Thread(target=accept_conexoes)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()