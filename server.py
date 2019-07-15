from threading import Thread
from SecureSocketService import Socket


class Server(Socket):
    def __init__(self, host: str = "localhost", port: int = 3621, service_id: int = 2):
        super().__init__()
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.service_id = service_id
        self.clients = dict()
        Thread(target=self.connexion).start()

    def connexion(self):
        while True:
            c, adress = self.connect_client(self.socket)
            name = self.client_name(c)
            if name:
                self.clients[name] = c
                self.broadcast(f"{name} is online !")
                Thread(target=self.listen_client, args=(name,)).start()

    def client_name(self, sock):
        while True:
            try:
                self.send(sock, "Your name ?")
                name = self.receive(sock)
                if name in self.clients:
                    self.send(sock, "Name already taken !")
                elif name.lower() == "quit":
                    sock.close()
                    name = None
                else:
                    break
            except:
                name = None
                break
        return name

    def listen_client(self, name):
        while True:
            try:
                data = self.receive(self.clients[name])
                assert data.lower() != "quit"
            except:
                self.send(self.clients[name], "quit")
                self.clients[name].close()
                del self.clients[name]
                self.broadcast(f"{name} is offline !")
                break
            else:
                Thread(target=self.broadcast, args=(f"{name}: {data}", name)).start()

    def broadcast(self, message, author = None):
        print(message)
        for i in self.clients:
            if i == author:
                continue
            try:
                self.send(self.clients[i], message)
            except:
                pass


if __name__ == "__main__":
    Server()
