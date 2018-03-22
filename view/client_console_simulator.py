import tkinter as tk
from services.client import Client


class ClientConsoleSimulator:
    WIDTH = 100
    PREFIX_TEXT = '>> '

    def __init__(self, hostname, port):
        self.window = None
        self.client = Client(hostname, port)

    def _get_label_template(self, text):
        return tk.Label(self.window, text=text, fg="white", bg="black", anchor=tk.W, justify=tk.LEFT,
                        width=self.WIDTH, font=('Consolas', 10))

    def _handle_entry_value(self, event):
        element_entry = event.widget
        value = str(element_entry.get())
        value = str.replace(value, self.PREFIX_TEXT.strip(), '').strip()

        # last text typed
        label = self._get_label_template(self.PREFIX_TEXT + value)
        label.pack(side='top', expand=0)

        # text got from server
        label = self._get_label_template(self.PREFIX_TEXT + self.client.request(value))
        label.pack(side='top', expand=0)

        element_entry.destroy()
        self._create_new_main_entry()

    def _create_new_main_entry(self):
        entry = tk.Entry(self.window, fg="white", bg="black", width=self.WIDTH, cursor='xterm',
                         insertbackground='white', font=('Consolas', 10))
        entry.bind("<Return>", self._handle_entry_value)
        entry.insert(tk.END, self.PREFIX_TEXT)
        entry.pack(side="top", expand=0)
        entry.focus_set()

    def open(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.wm_title("Client Console acessando %s:%s" % (self.client.host, self.client.port))
        self.window.configure(background='black')
        self.window.minsize(self.WIDTH, 400)
        self._get_label_template(self.PREFIX_TEXT + 'Available commands: ' + self.client.request('?')).pack(side='top',
                                                                                                            expand=0)
        self._create_new_main_entry()

    def close(self):
        self.window.destroy()

    def is_active(self):
        return self.window.winfo_exists()


