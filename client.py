from threading import Thread
from SecureSocketService import Socket
from sys import exit
from socket import error as socket_error


class Client(Socket):
    def __init__(self, host: str, port: int, service_id: int = 2):
        super().__init__()
        self.service_id = service_id
        print("Connecting...")
        self.connect_server(host, port)
        Thread(target=self.receive_server).start()
        Thread(target=self.send_input).start()

    def receive_server(self):
        while True:
            try:
                data = self.receive(self.socket)
            except socket_error:
                self.quit()
            else:
                if data.lower() == "quit":
                    self.quit()
                    break
                print(data)

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

    def quit(self):
        try:
            self.socket.close()
        except socket_error:
            pass
        finally:
            print("Disconnected")
            exit()


if __name__ == "__main__":
    Client("localhost", 3621)
