import socket


class Client:
    def __init__(self, server_domain='localhost', server_port=50007):
        self.host = server_domain
        self.port = server_port

    def request(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.sendall(command.encode())
        data = s.recv(1024)
        s.close()
        return data.decode()
