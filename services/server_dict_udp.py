import socket
from services.server import Server


class ServerDictUDP(Server):
    def __init__(self, domain='localhost', port=50007):
        super().__init__(domain, port)
        self.host = domain
        self.port = port
        self.INVALID_COMMAND_MSG = "Comando invalido, verifique os possiveis comandos com \"?\""
        self.DICT_COMMANDS = {
            'ADD': self.get_add_info,
            'DEL': self.get_del_info,
            'GET': self.get_get_info,
            'STORAGE': self.get_storage,
            'application_name': self.get_app_name
        }
        commands = self.COMMANDS.copy()
        commands.update(self.DICT_COMMANDS)
        self.ALL_COMMANDS = commands
        self.storage = {'application_name': 'Free Dictionary'}

    def _get_value_of_dict_command(self, command, data):
        value = data.replace(command, '', 1)
        return value.strip()

    def _get_from_storage(self, value):
        return self.storage.get(value, '[404] - Valor nao encontrado no Storage')

    def _delete_from_storage(self, value):
        if value in self.storage:
            return self.storage.pop(value)
        else:
            return self._get_from_storage(value)

    def _add_to_storage(self, value):
        words = value.split(':')
        if len(words) != 2:
            return 'Comando invalido, verifique o comando ADD e veja se voce passou a chave e o valor corretamente.'

        key = words[0].strip()
        val = words[1].strip()
        self.storage[key] = val
        return "STORAGE -> { ... , %s: %s }" % (key, val)

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        self.started = True
        while self.can_continue:
            data, addr = sock.recvfrom(1024)
            if not data:
                sock.sendto(self.INVALID_COMMAND_MSG.encode(), addr)
                continue

            data = data.decode().strip()
            func = self.COMMANDS.get(data)
            if func:
                result = func()
                sock.sendto(str(result).encode(), addr)
            else:
                func = self.DICT_COMMANDS.get(data)
                if func:
                    result = func()
                    sock.sendto(str(result).encode(), addr)
                else:
                    result = self.INVALID_COMMAND_MSG
                    if data.find('GET') == 0:
                        result = self._get_from_storage(self._get_value_of_dict_command('GET', data))
                    elif data.find('ADD') == 0:
                        result = self._add_to_storage(self._get_value_of_dict_command('ADD', data))
                    elif data.find('DEL') == 0:
                        result = self._delete_from_storage(self._get_value_of_dict_command('DEL', data))

                    sock.sendto(str(result).encode(), addr)

        sock.close()

    # override
    def available_commands(self):
        return list(self.ALL_COMMANDS.keys())

    def get_add_info(self):
        return "Para adicionar dados ao Storage, apenas digite 'ADD chave: valor'.\nEx.: ADD Carlos: 99119-7861\n"

    def get_del_info(self):
        return "Para deletar dados do Storage, apenas digite 'DEL chave'. O valor deletado sera retornado."

    def get_get_info(self):
        return "Para consular algum dado do Storage, apenas digite 'GET chave'"

    def get_app_name(self):
        return self.storage.get('application_name', 'Free Dictionary')

    def get_storage(self):
        return 'STORAGE -> ' + str(self.storage)
