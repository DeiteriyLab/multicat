import logging
from abc import ABC, abstractmethod
from typing import Dict
from celery import Celery
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    commands_info: Dict[str, str] = {}

    def __init__(self, bot: Bot, router: Router, app: Celery):
        self.bot = bot
        self.router = router
        self.app = app
        BaseCommand.commands_info[self.command] = self.description
        self.register_command_handler()

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def command(self):
        pass

    @abstractmethod
    async def handle(self, message: Message):
        pass

    def register_command_handler(self):
        @self.router.message(Command(self.command))
        async def inner_command_handler(message: Message):
            try:
                await self.handle(message)
            except Exception as e:
                logger.error(
                    "Error handling command %s: %s", self.command, e, exc_info=True
                )
                await message.reply("Something went wrong. Please try again later.")
