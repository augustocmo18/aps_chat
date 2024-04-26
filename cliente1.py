from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread
from PIL import Image, ImageTk
import io
import tkinter
from tkinter import filedialog
import base64

ip = None
msg = None

def send_message(message):
    con_tcp.send(bytes(message, "utf8"))

def send_image():
    if image_path:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            encoded_image = base64.b64encode(image_data)
            # encoded_image_pad = add_padding(encoded_image)
            con_tcp.send(b"IMAGE:" + encoded_image)
            return  
    else:
        msg_list.insert(tkinter.END, "SISTEMA: Nenhuma imagem selecionada!")

def add_padding(encoded_image):
    try:
        missing_padding = len(encoded_image) % 4
        if missing_padding != 0:
            encoded_image += '=' * (4 - missing_padding)
        return encoded_image
    except Exception as e:
        print("Error adding padding:", e)
        return None



def display_image(encoded_image):
    try:
        image_data = base64.b64decode(encoded_image)
        image_stream = io.BytesIO(image_data)
        image = Image.open(image_stream)
        root = tkinter.Tk()
        photo = ImageTk.PhotoImage(image)
        image_label = tkinter.Label(root, image=photo)
        image_label.photo = photo 
        image_label.pack()
        def close_img():
            root.quit()
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", close_img)
        root.mainloop()
    except Exception as e:
        print("Error displaying image:", e)

def set_image_path():
    global image_path
    image_path = filedialog.askopenfilename()

def chat():
    mensagem.set(e_mensagem.get())
    msg = mensagem.get()
    if msg is not None:
        if (msg.lower() == 'exit'):
            fecha()
            return
        send_message(msg)
        e_mensagem.delete(0, tkinter.END)

def chatrecebe():
        while True:
            try:
                recv_broad = con_tcp.recv(650724).decode("utf8")
                if recv_broad:
                    if recv_broad.startswith("IMAGE:"):
                        image_data = recv_broad[len("IMAGE:"):]
                        display_image(image_data)
                        return
                    else:
                        if len(recv_broad) > 1:
                            msg_list.insert(tkinter.END, recv_broad)
                            print(recv_broad)
            except OSError:
                break





def fecha():
    mensagem.set("exit")
    msg = mensagem.get()
    con_tcp.send(bytes(msg, "utf8"))
    window.quit()
    window.destroy()
    
    
def set_ip():
    global ip
    ip = ips.get()
    print(ip)
    windowip.quit()
    windowip.destroy()

def get_ip():
    global ip
    return ip
    

     

#interface grafica
windowip = tkinter.Tk()
windowip.title("IpBox")
windowip.configure(bg="#ffffff")
windowip.geometry("230x150")  # tamanho e psocionamento
windowip.resizable(False, False)

windowip.protocol("WM_DELETE_WINDOW", fecha)


ips = tkinter.StringVar()  # declarando o tipo do campo mensagem
l_digiteip = tkinter.Label(windowip, text="Digite o ip do servidor: ", font="Ubuntu 14", height=2, bg="#ffffff")
e_mensagemip = tkinter.Entry(windowip, font="Ubuntu 12 bold", fg="#483659", width=25, textvariable=ips)
e_mensagemip.bind("<Return>", )
b_enviarip = tkinter.Button(windowip, text="Conectar", font="Ubuntu 14 bold", height=1, border=3,
                          relief="groove", fg="#483659", command=set_ip)

l_digiteip.grid(row=1, column=0, padx=5, pady=5)
e_mensagemip.grid(row=20, column=0)
b_enviarip.grid(row=25,sticky='sew', padx=5, pady=5)



window = tkinter.Tk()
window.title("ChatBox1")
window.configure(bg="#ffffff")
window.geometry("475x550")  # tamanho e psocionamento
window.resizable(False, False)

window.protocol("WM_DELETE_WINDOW", fecha)

campo_conversa = tkinter.Frame(window, height=150)
mensagem = tkinter.StringVar()  # declarando o tipo do campo mensagem
scrollbar = tkinter.Scrollbar(campo_conversa)
l_mensagem = tkinter.Label(window, text="Mensagem:", font="Ubuntu 14", width=10, height=2, bg="#ffffff")
l_conversa = tkinter.Label(window, text=" Conversa: ", font="Ubuntu 14", height=2, bg="#ffffff")
msg_list = tkinter.Listbox(window, height=15, width=50, font="Ubuntu 12 bold", fg="#483659", border=2,
                           yscrollcommand=scrollbar.set)
e_mensagem = tkinter.Entry(window, font="Ubuntu 12 bold", fg="#483659", width=50, textvariable=mensagem)
e_mensagem.bind("<Return>", )
b_enviar = tkinter.Button(window, text="Enviar Mensagem", font="Ubuntu 14 bold", height=1, border=3,
                          relief="groove", fg="#483659", command=chat)
b_sair = tkinter.Button(window, text="Exit", font="Ubuntu 14 bold", fg="red", border=3, relief='groove',
                        command=fecha)
b_set_image_path = tkinter.Button(window, text="Escolher Imagem", font="Ubuntu 14 bold", height=1, border=3,
                                   relief="groove", fg="#483659", command=set_image_path)
b_img = tkinter.Button(window, text="Enviar Imagem", font="Ubuntu 14 bold", height=1, border=3,
                                   relief="groove", fg="#483659", command=send_image)


b_img.grid(row=30, sticky='e', padx=5, pady=5)
b_set_image_path.grid(row=30, sticky='w', padx=5, pady=5)
scrollbar.grid()
msg_list.grid(row=2, column=0)
campo_conversa.grid(row=2, column=1)
l_mensagem.grid(row=4, column=0, pady=5, sticky='w')
l_conversa.grid(row=1, column=0, padx=5, pady=5)
e_mensagem.grid(row=20, column=0)
b_enviar.grid(row=25,sticky='w', padx=5, pady=5)
b_sair.grid(row=25, sticky='e', pady=5)
            

SERVER_PORT = 9050

msg_list.insert(tkinter.END, "Bem vindo ao Chat sem nome no momento!\n")
windowip.mainloop()
ADDR = (get_ip(), SERVER_PORT)
con_tcp = socket(AF_INET,SOCK_STREAM)
con_tcp.connect(ADDR)
print("conectado")
msg_list.insert(tkinter.END, "Chat iniciado! Para sair escreva: exit ")
msg_list.insert(tkinter.END, "Escreva seu nome: ")
while True:
    receive_thread = Thread(target=chatrecebe)
    receive_thread.start()
    window.mainloop()
