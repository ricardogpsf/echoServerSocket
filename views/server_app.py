from services import client, server, client_dict_udp, server_dict_udp
import tkinter as tk
import threading


class ServerApp:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def _create_widgets(self):
        tk.Label(self.window, text="Servidor executando em %s:%s" % (self.hostname, self.port)).pack(padx=10)
        tk.Button(self.window, text="Encerrar", command=self._close_and_quit_server).pack(pady=10)

    def _start_server(self, callback_error):
        self.server_instance = server_dict_udp.ServerDictUDP(self.hostname, self.port)
        try:
            self.server_instance.start()
        except Exception as error:
            callback_error(error)

    def _close_and_quit_server(self):
        self.server_instance.teminate()
        if self.server_instance.started:
            client_dict_udp.ClientDictUDP(self.hostname, self.port).request('') # it is just for forcing the closing of server

        self.window.destroy()

    def open(self, parent, callback_error=None):
        self.window = tk.Toplevel(parent)
        self.window.wm_title("ServerApp")
        self.window.minsize(200, 40)
        self.window.protocol("WM_DELETE_WINDOW", self._close_and_quit_server)
        self._create_widgets()
        threading.Thread(None, target=self._start_server, args=(callback_error, )).start()

    def close(self):
        self._close_and_quit_server()

    def is_active(self):
        return self.window.winfo_exists()
