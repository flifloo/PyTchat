from threading import Thread
from SecureSocketService import Socket
from sys import exit


class Client(Socket):
    def __init__(self, host: str, port: int, service_id: int = 2):
        super().__init__()
        self.service_id = service_id
        print("Connecting...")
        self.connect_server(host, port)
        self.receive_th = Thread(target=self.receive_server).start()
        self.send_th = Thread(target=self.send_server).start()

    def receive_server(self):
        while True:
            data = self.receive(self.socket)
            if data.lower() == "quit":
                self.quit()
                break
            print(data)

    def send_server(self):
        while True:
            data = input()
            self.send(self.socket, data)
            if data.lower() == "quit":
                break

    def quit(self):
        self.socket.close()
        print("Exit")
        exit()


if __name__ == "__main__":
    Client("localhost", 3621)
