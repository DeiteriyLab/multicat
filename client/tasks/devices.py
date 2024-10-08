import logging

from celery import shared_task, signature

from config import Config, Database
from filemanager import AssetsFileManager
from hashcat import HashcatDevices
from hashcat.hashcat import Hashcat

logger = logging.getLogger(__name__)
db = Database(Config().database_url)
file_manager = AssetsFileManager()
hashcat = Hashcat()
hashcat_devices = HashcatDevices(file_manager, hashcat)


def _update_devices():
    worker_name = Config().worker_name
    devices_obj = hashcat_devices.devices_info()
    signature(
        "server.update_devices_info", queue="server", args=(worker_name, devices_obj)
    ).apply_async()


@shared_task(name="b.update_devices", ignore_result=True)
def update_devices():
    _update_devices()
