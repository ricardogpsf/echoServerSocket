from services import client, server
import tkinter as tk
import threading


class ServerApp():
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def _create_widgets(self):
        tk.Label(self.window, text="Servidor executando em %s:%s" % (self.hostname, self.port)).pack(padx=10)
        tk.Button(self.window, text="Encerrar", command=self._close_and_quit_server).pack(pady=10)

    def _start_server(self):
        self.server_instance = server.Server(self.hostname, self.port)
        self.server_instance.start()

    def _close_and_quit_server(self):
        self.server_instance.teminate()
        client.Client(self.hostname, self.port).request('') # it is just for forcing the closing of server
        self.window.destroy()

    def open(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.wm_title("ServerApp")
        self.window.minsize(200, 40)
        self.window.protocol("WM_DELETE_WINDOW", self._close_and_quit_server)
        self._create_widgets()
        threading.Thread(None, self._start_server).start()

    def close(self):
        self._close_and_quit_server()

    def is_active(self):
        return self.window.winfo_exists()
