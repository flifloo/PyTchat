from threading import Thread
from SecureSocketService import Socket
from socket import error as socket_error


class Client(Socket):
    def __init__(self, host: str, port: int, service_id: int = 2):
        super().__init__()
        self.service_id = service_id
        self.connect_server(host, port)

    def receive_server(self):
        try:
            data = self.receive(self.socket)
        except socket_error:
            self.quit()
            return False
        else:
            if data.lower() == "quit":
                self.quit()
                return False
            return data

    def send_server(self, data):
        try:
            self.send(self.socket, data)
        except socket_error:
            self.quit()

    def send_input(self):
        while True:
            data = input()
            self.send_server(data)
            if data.lower() == "quit":
                break

    def receive_print(self):
        while True:
            message = self.receive_server()
            if message:
                print(message)
            else:
                break

    def quit(self):
        try:
            self.socket.close()
        except socket_error:
            pass


if __name__ == "__main__":
    client = Client("localhost", 3621)
    Thread(target=client.receive_print).start()
    Thread(target=client.send_input).start()
