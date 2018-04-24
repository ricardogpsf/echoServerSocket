import socket


class ClientDictUDP:
    def __init__(self, server_domain='localhost', server_port=50007):
        self.host = server_domain
        self.port = server_port

    def request(self, command):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(command.encode(), (self.host, self.port))
        data = s.recv(1024)
        return data.decode()
