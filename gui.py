from tkinter import Tk, Frame, Scrollbar, Label, Text, Button, Entry, StringVar, IntVar, TclError
from tkinter.messagebox import showerror, showwarning
from client import Client
from threading import Thread
from socket import error as socket_error

destroy = False


def on_closing():
    global destroy
    destroy = True
    try:
        client.send_server("quit")
    except TclError:
        pass
    finally:
        try:
            tchat.destroy()
        except TclError:
            pass


def start():
    if host.get() and port.get():
        try:
            global client
            client = Client(host.get(), port.get())
        except (socket_error, ConnectionError):
            showerror("Error", "Can't connect to server !")
        else:
            login.destroy()


def receive():
    while True:
        try:
            msg = client.receive_server()
            if msg.lower() == "quit" or not msg:
                raise ConnectionError("Client quit")
        except (socket_error, ConnectionError, AttributeError):
            show_message("""}------------------------------{
/!\\ [Receive system offline] /!\\
Press Enter to exit
}------------------------------{""")
            break
        else:
            show_message(msg)


def send(event=None):
    try:
        client.send_server(message.get())
        if not receive_thread.is_alive() or message.get().lower() == "quit":
            raise ConnectionError("Client quit")
    except (socket_error, ConnectionError):
        showwarning("Disconnected", "Disconnected from server")
        on_closing()
    else:
        message.set("")


def show_message(msg):
    if msg[-1:] != "\n":
        msg += "\n"
    if not destroy:
        chat_message.configure(state="normal")
        chat_message.insert("end", msg)
        chat_message.configure(state="disable")


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
receive_thread = Thread(target=receive)
receive_thread.start()

entry = Frame(tchat)
entry.pack()
message = StringVar()
field = Entry(entry, textvariable=message)
field.bind("<Return>", send)
field.grid(row=0, column=0)
Button(entry, text="Send", command=send).grid(row=0, column=1)
tchat.mainloop()
