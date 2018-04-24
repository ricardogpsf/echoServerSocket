import tkinter as tk
from views.client_console_simulator import ClientConsoleSimulator
from views.server_app import ServerApp


class Application(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.message_label = None
        self.hostname_entry = None
        self.port_entry = None
        self.client_consoles = []
        self.server_apps = []
        self.master.minsize(300, 150)
        self.grid()
        self.create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self._close_and_clear_all)

    def _close_and_clear_all(self):
        self._close_apps(self.server_apps)
        self._close_apps(self.client_consoles)
        self.quit()

    def _close_apps(self, apps):
        for app in apps:
            if app.is_active():
                app.close()

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
            server_app = ServerApp(
                self.hostname_entry.get(), int(self.port_entry.get()))
            self.server_apps.append(server_app)

            def callback_error(error):
                server_app.close()
                self.message_label.configure(text=str(error), fg='red')

            server_app.open(self, callback_error)

    def init_client(self):
        if self.required_fields_are_valid():
            client_console = ClientConsoleSimulator(self.hostname_entry.get(), int(self.port_entry.get()))
            self.client_consoles.append(client_console)

        try:
            client_console.open(self)
        except Exception as error:
            client_console.close()
            self.message_label.configure(text=str(error), fg='red')
