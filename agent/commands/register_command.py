class CommandRegistry:
    def __init__(self):
        self._commands = []

    def register(self, cls):
        self._commands.append(cls)
        return cls

    def list_commands(self):
        return self._commands


command_registry = CommandRegistry()


def register_command(cls):
    return command_registry.register(cls)
