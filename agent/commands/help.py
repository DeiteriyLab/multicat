from aiogram.types import Message
from commands import BaseCommand

from .register_command import register_command


@register_command
class Help(BaseCommand):
    @property
    def command(self):
        return "help"

    @property
    def description(self):
        return "Print this message"

    async def handle(self, message: Message):
        help_message = "Доступные команды:\n"
        for command, description in BaseCommand.commands_info.items():
            help_message += f"/{command} - {description}\n"
        await message.answer(help_message)
