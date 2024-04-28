from socket import AF_INET, socket, SOCK_STREAM, gethostname, gethostbyname
from threading import Thread
import tkinter
from tkinter import filedialog
import base64

ip = None
msg = None
image_path = None
con_tcp = None

def send_message(message):
    con_tcp.send(bytes(message, "utf8"))

def send_image(img):
    encoded_image = base64.b64encode(img)
    img_transmit = (b"IMAGE:" + encoded_image)
    con_tcp.send(img_transmit)
    
def fecha():
    mensagem.set("exit")
    msg = mensagem.get()
    con_tcp.send(bytes(msg, "utf8"))
    window.quit()
    window.destroy()
    
#criação das janelas
window = tkinter.Tk()
window.title("ChatBox1")
window.configure(bg="#ffffff")
window.geometry("475x550")  
window.resizable(False, False)

window.protocol("WM_DELETE_WINDOW", fecha)

windowip = tkinter.Toplevel(window)
windowip.title("IpBox")
windowip.configure(bg="#ffffff")
windowip.geometry("230x150")  
windowip.resizable(False, False)

windowip.protocol("WM_DELETE_WINDOW", fecha)

def set_image_path():
    global image_path
    image_path = filedialog.askopenfilename()

def image():
    global image_path
    if image_path:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            send_image(image_data)
            image_path = None
            image_data = None
    else:
        msg_text.insert(tkinter.END, "SISTEMA: Nenhuma imagem selecionada!\n")

def chat(event=None):
    mensagem.set(e_mensagem.get())
    msg = mensagem.get()
    if msg is not None:
        if (msg.lower() == 'exit'):
            fecha()
            return
        send_message(msg)
        e_mensagem.delete(0, tkinter.END)

def ask_to_save_image(image_data):
    if tkinter.messagebox.askyesno("Salvar Imagem", "Deseja salvar a imagem recebida?"):
        try:
            imgtosave = base64.b64decode(image_data)
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if file_path:
                try:
                    with open(file_path, "wb") as f:
                            f.write(imgtosave)
                            msg_text.insert(tkinter.END, "Imagem salva com sucesso!\n")
                except Exception as e:
                    print("Error saving image:", e)
        except Exception as e:
            print("Error saving image:", e)

def chatrecebe():
        while True:
            try:
                recv_broad = con_tcp.recv(650724).decode("utf8")
                if recv_broad:
                    if recv_broad.startswith("IMAGE:"):
                        image_data = recv_broad[len("IMAGE:"):]
                        msg_text.insert(tkinter.END, "Imagem recebida! Clique aqui para salvar.\n")
                        msg_text.tag_add("save_image", "end-1c", "end")
                        msg_text.tag_configure("save_image", foreground="blue", underline=True)
                        msg_text.bind("<Button-1>", lambda event, image_data=image_data: ask_to_save_image(image_data))
                        scroll_text()
                        continue
                    else:
                        if len(recv_broad) > 1:
                            msg_text.insert(tkinter.END, recv_broad + "\n")
                            scroll_text()
                            print(recv_broad)
            except Exception as e:
                print("Error in chatrecebe:", e)
                break  

def set_ip():
    global ip
    ip = ips.get()
    print(ip)
    windowip.quit()
    windowip.destroy()

def get_ip():
    global ip
    return ip
    
def scroll_text(*args):
    msg_text.yview_moveto(1.0)

#interface grafica
ips = tkinter.StringVar()  

l_digiteip = tkinter.Label(windowip, text="Digite o ip do servidor: ", font="Ubuntu 14", height=2, bg="#ffffff")
e_mensagemip = tkinter.Entry(windowip, font="Ubuntu 12 bold", fg="#483659", width=25, textvariable=ips)
e_mensagemip.bind("<Return>", lambda event: b_enviarip.invoke())
b_enviarip = tkinter.Button(windowip, text="Conectar", font="Ubuntu 14 bold", height=1, border=3,
                          relief="groove", fg="#483659", command=set_ip)


campo_conversa = tkinter.Frame(window, height=150)
mensagem = tkinter.StringVar()  
l_mensagem = tkinter.Label(window, text="Mensagem:", font="Ubuntu 14", width=10, height=2, bg="#ffffff")
l_conversa = tkinter.Label(window, text=" Conversa: ", font="Ubuntu 14", height=2, bg="#ffffff")
msg_text = tkinter.Text(window, height=15, width=50, font="Ubuntu 12 bold", fg="#483659")
scrollbar = tkinter.Scrollbar(window, command=msg_text.yview)
msg_text.bind("<Key>", scroll_text)
msg_text.configure(yscrollcommand=scrollbar.set)
e_mensagem = tkinter.Entry(window, font="Ubuntu 12 bold", fg="#483659", width=50, textvariable=mensagem)
e_mensagem.bind("<Return>", lambda event: (chat(), scroll_text()))
b_enviar = tkinter.Button(window, text="Enviar Mensagem", font="Ubuntu 14 bold", height=1, border=3,
                          relief="groove", fg="#483659", command=chat)
b_sair = tkinter.Button(window, text="Exit", font="Ubuntu 14 bold", fg="red", border=3, relief='groove',
                        command=fecha)
b_set_image_path = tkinter.Button(window, text="Escolher Imagem", font="Ubuntu 14 bold", height=1, border=3,
                                   relief="groove", fg="#483659", command=set_image_path)
b_img = tkinter.Button(window, text="Enviar Imagem", font="Ubuntu 14 bold", height=1, border=3,
                                   relief="groove", fg="#483659", command=image)

l_digiteip.grid(row=1, column=0, padx=5, pady=5)
e_mensagemip.grid(row=20, column=0)
b_enviarip.grid(row=25,sticky='sew', padx=5, pady=5)
scrollbar.grid(row=2, sticky='nse')
b_img.grid(row=30, sticky='e', padx=5, pady=5)
b_set_image_path.grid(row=30, sticky='w', padx=5, pady=5)
msg_text.grid(row=2, column=0)
campo_conversa.grid(row=2, column=1)
l_mensagem.grid(row=4, column=0, pady=5, sticky='w')
l_conversa.grid(row=1, column=0, padx=5, pady=5)
e_mensagem.grid(row=20, column=0)
b_enviar.grid(row=25,sticky='w', padx=5, pady=5)
b_sair.grid(row=25, sticky='e', pady=5)
            

def main():
    global con_tcp
    SERVER_PORT = 9050

    msg_text.insert(tkinter.END, "Bem vindo ao Chat sem nome no momento!\n")
    windowip.mainloop()
    ADDR = (get_ip(), SERVER_PORT)
    con_tcp = socket(AF_INET,SOCK_STREAM)
    con_tcp.connect(ADDR)
    print("conectado")
    msg_text.insert(tkinter.END, "Chat iniciado! Para sair escreva: exit \n")
    msg_text.insert(tkinter.END, "Escreva seu nome: \n")
    receive_thread = Thread(target=chatrecebe)
    receive_thread.start()
    window.mainloop()
    

if __name__ == "__main__":
    main()
