import os
import platform
import socket
import time


class Server:
    def __init__(self, domain='localhost', port=50007):
        self.host = domain
        self.port = port
        self.COMMANDS = {'?': self.available_commands,
                         'date': self.get_date,
                         'hostname': self.get_hostname,
                         'username': self.get_logged_user,
                         'system info': self.get_uname,
                         'python version': self.get_python_version}
        self.can_continue = True
        self.started = False

    def teminate(self):
        self.can_continue = False

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(1)
        self.started = True

        while self.can_continue:
            conn, addr = s.accept()
            print('Connected by', addr)
            while self.can_continue:
                data = conn.recv(1024)
                if not data: break
                func = self.COMMANDS.get(data.decode())
                if func:
                    result = func()
                    conn.sendall(str(result).encode())
                else:
                    conn.sendall(b'Comando invalido, verifique os possiveis comandos "?"')
            conn.close()

    def available_commands(self):
        return list(self.COMMANDS.keys())

    def get_date(self):
        return time.strftime('%d/%m/%Y %H:%m:%S')

    def get_logged_user(self):
        return os.getlogin()

    def get_hostname(self):
        return os.getenv('UserDomain')

    def get_uname(self):
        return platform.uname()

    def get_python_version(self):
        return platform.python_version()
