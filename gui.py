from tkinter import Tk, Frame, Scrollbar, Label, Text, Button, Entry, StringVar, IntVar
from tkinter.messagebox import showerror
from client import Client
from threading import Thread


def on_closing():
    try:
        client.quit()
    except NameError:
        pass


def start():
    if host.get() and port.get():
        try:
            global client
            client = Client(host.get(), port.get())
        except ConnectionError:
            showerror("Error", "can't connect to server !")
        else:
            login.destroy()


def receive():
    while True:
        msg = client.receive_server()
        if msg.lower() == "quit":
            break
        if msg[-1:] != "\n":
            msg += "\n"
        chat_message.configure(state="normal")
        chat_message.insert("end", msg)
        chat_message.configure(state="disable")


def send(event=None):
    client.send_server(message.get())
    if message.get().lower() == "quit":
        tchat.destroy()
    message.set("")


login = Tk()
login.title("Login")
host = StringVar()
port = IntVar()
Label(login, text="Host & port:").pack()
login_f = Frame(login)
login_f.pack()
Entry(login_f, textvariable=host, width=14).grid(row=0, column=0)
Entry(login_f, textvariable=port, width=4).grid(row=0, column=1)
Button(login, text="Submit", command=start).pack()
login.mainloop()

tchat = Tk()
tchat.title("PyTchat")
tchat.protocol("WM_DELETE_WINDOW", on_closing)
chat = Frame(tchat)
chat.pack()
scrollbar = Scrollbar(chat)
scrollbar.pack(side="right", fill="y")
chat_message = Text(chat, height=15, width=50, yscrollcommand=scrollbar.set, state="disable")
chat_message.pack(side="left", fill="both")
Thread(target=receive).start()

entry = Frame(tchat)
entry.pack()
message = StringVar()
field = Entry(entry, textvariable=message)
field.bind("<Return>", send)
field.grid(row=0, column=0)
Button(entry, text="Send", command=send).grid(row=0, column=1)
tchat.mainloop()
