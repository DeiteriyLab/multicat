from celery import Celery
from kombu import Exchange, Queue
from kombu.common import Broadcast

from .config import Config


class CeleryApp:
    def __init__(self, name):
        self.app = Celery(name)
        self.configure_celery()

    def configure_celery(self):
        broadcast_exchange = Exchange("broadcast_exchange", type="fanout")
        default_exchange = Exchange("default", type="direct")

        self.app.conf.task_queues = (
            Queue("client", exchange=default_exchange, routing_key="main.#"),
            Broadcast("broadcast", exchange=broadcast_exchange),
        )

        self.app.conf.task_default_queue = "client"
        self.app.conf.task_default_exchange = "default"
        self.app.conf.task_routes = {
            "b.*": {"queue": "broadcast"},
            "*": {"queue": "client"},
        }

        self.app.conf.update(
            broker_url=Config.get("CELERY_BROKER_URL"),
            result_backend=Config.get("CELERY_RESULT_BACKEND"),
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone=Config.get("TIMEZONE"),
            enable_utc=True,
        )

    def get_app(self):
        return self.app
