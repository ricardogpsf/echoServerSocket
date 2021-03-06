import tkinter as tk
from services.client import Client
from services.client_dict_udp import ClientDictUDP


class ClientConsoleSimulator:
    WIDTH = 200
    PREFIX_TEXT = '>> '

    def __init__(self, hostname, port):
        self.window = None
        self.client = ClientDictUDP(hostname, port)
        self.elements_added = []

    def _clear_panel(self):
        for element in self.elements_added:
            element.destroy()

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
        self.elements_added.append(label)

        if value == 'clear':
            self._clear_panel()
        else:
            # text got from server
            label = self._get_label_template(self.PREFIX_TEXT + self.client.request(value))
            label.pack(side='top', expand=0)
            self.elements_added.append(label)

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
        # in the time of first request, it is moment that can occur an error
        self._get_label_template(self.PREFIX_TEXT + 'Available commands: ' + self.client.request('?')).pack(
            side='top',
            expand=0)
        self._create_new_main_entry()

    def close(self):
        self.window.destroy()

    def is_active(self):
        return self.window.winfo_exists()
