import tkinter as tk
from views.client_console_simulator import ClientConsoleSimulator
from views.server_app import ServerApp


class Application(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.message_label = None
        self.hostname_entry = None
        self.port_entry = None
        self.client_console = None
        self.server_app = None
        self.master.minsize(300, 150)
        self.grid()
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self._close_and_clear_all)

    def _close_and_clear_all(self):
        if self.client_console and self.client_console.is_active():
            self.client_console.close()

        if self.server_app and self.server_app.is_active():
            self.server_app.close()

        self.quit()

    def create_widgets(self):
        self.message_label = tk.Label(self, text='')
        self.message_label.grid(column=0, row=0, columnspan=3)

        tk.Label(self, text='Hostname:').grid(column=0, row=1)
        self.hostname_entry = tk.Entry(self, width=20)
        self.hostname_entry.insert(tk.END, 'localhost')
        self.hostname_entry.grid(column=1,row=1)

        tk.Label(self, text='Porta:').grid(column=0, row=2)
        self.port_entry = tk.Entry(self, width=20)
        self.port_entry.insert(tk.END, '50002')
        self.port_entry.grid(column=1, row=2)

        tk.Button(self, text='Iniciar servidor', command=self.init_server).grid(column=0, row=4, pady=20, padx=10)
        tk.Button(self, text='Iniciar console de cliente', command=self.init_client).grid(column=1, row=4, pady=20, padx=10)

    def required_fields_are_valid(self):
        hostname = self.hostname_entry.get()
        port = self.port_entry.get()
        if not hostname or not port or not port.isdigit():
            self.message_label.configure(text='Digite o hostname e a porta corretamente', fg='red')
            return False

        return True

    def init_server(self):
        if self.required_fields_are_valid():
            self.server_app = ServerApp(self.hostname_entry.get(), int(self.port_entry.get()))
            self.server_app.open(self)

    def init_client(self):
        if self.required_fields_are_valid():
            self.client_console = ClientConsoleSimulator(self.hostname_entry.get(), int(self.port_entry.get()))
            try:
                self.client_console.open(self)
            except:
                self.client_console.close()
                self.message_label.configure(text='Não foi possível conectar ao servidor', fg='red')
