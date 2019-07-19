from threading import Thread
from SecureSocketService import Socket
from socket import error as socket_error


class Server(Socket):
    def __init__(self, host: str = "localhost", port: int = 3621, service_id: int = 2):
        print("Server start")
        super().__init__()
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.service_id = service_id
        self.command_suffix = "/"
        self.welcome_msg = "Welcome ! Type \"/help\" to see commands and \"quit\" to exit"
        self.commands = {"help": self.command_help, "players list": self.command_players_list}
        self.clients = dict()
        print("Wait for connexion...")
        Thread(target=self.connexion).start()

    def connexion(self):
        while True:
            try:
                c, address = self.connect_client(self.socket)
            except (socket_error, ConnectionError):
                continue
            else:
                name = self.client_name(c)
                if name:
                    self.clients[name] = c
                    self.send(self.clients[name], self.welcome_msg)
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
            except socket_error:
                name = None
                break
        return name

    def listen_client(self, name):
        while True:
            try:
                data = self.receive(self.clients[name])
                assert data.lower() != "quit"
            except (socket_error, AssertionError):
                self.client_quit(name)
                break
            else:
                if not self.command(data, name):
                    Thread(target=self.broadcast, args=(f"{name}: {data}",)).start()

    def broadcast(self, message):
        print(message)
        for i in self.clients:
            try:
                self.send(self.clients[i], message)
            except socket_error:
                continue

    def client_quit(self, name):
        try:
            self.send(self.clients[name], "quit")
            self.clients[name].close()
        except socket_error:
            pass
        finally:
            del self.clients[name]
            self.broadcast(f"{name} is offline !")

    def command(self, command, author):
        command = command.lower()
        if (command[:1] == self.command_suffix) and (command[1:] in self.commands):
            command = command[1:]
        elif command[:1] == self.command_suffix:
            command = "help"
        else:
            return False

        try:
            print(f"{author} use command {command}")
            self.commands[command](author)
        except socket_error:
            self.client_quit(author)
        finally:
            return True

    def command_help(self, author):
        message = "[Help]"
        for i in self.commands:
            message += "\n- " + i
        self.send(self.clients[author], message)

    def command_players_list(self, author):
        message = f"[Players list | {len(self.clients)} online]"
        for i in self.clients:
            message += "\n- " + i
        self.send(self.clients[author], message)


if __name__ == "__main__":
    Server()
