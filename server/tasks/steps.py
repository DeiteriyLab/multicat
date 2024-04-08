import logging
from typing import List

from celery import shared_task

from config import Database, UUIDGenerator
from db import DatabaseHelper, StepManager
from models.keyspaces import Keyspace
from schemas import CeleryResponse

logger = logging.getLogger(__name__)


db = Database()


@shared_task(name="server.delete_steps")
def delete_steps(user_id: str, step_name: int):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        manager.delete_steps(step_name)
        return CeleryResponse(value="Step deleted successfully").model_dump()


@shared_task(name="server.get_steps")
def get_steps(user_id: str, step_name: str):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        yaml_dump = manager.get_steps(step_name)
        return CeleryResponse(value=yaml_dump).model_dump()


@shared_task(name="server.list_steps")
def list_steps(user_id: str):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        steps_name = manager.list_steps()
        return CeleryResponse(value=steps_name).model_dump()


@shared_task(name="server.load_steps")
def load_steps(user_id: str, steps_name: str, yaml_content: str):
    user_id = str(UUIDGenerator.generate(user_id))
    with db.session() as session:
        manager = StepManager(user_id, session)
        manager.load_steps(steps_name, yaml_content)
        return CeleryResponse(value=f"{steps_name} saved successfully").model_dump()


@shared_task(name="server.post_load_steps")
def post_load_steps(keyspaces, unkown_keyspaces: List = list(), user_id: str = "", steps_name: str = ""):
    print(keyspaces)
    with db.session() as session:
        for keyspace, value in zip(unkown_keyspaces, keyspaces):
            keyspace["value"] = value

            ks = Keyspace(**keyspace)
            session.add(ks)

        db_helper = DatabaseHelper(session)
        step = db_helper.get_steps(user_id, steps_name)
        step.is_keyspace_calculated = True
        session.commit()

    # TODO: Notify user about what happend (not in the world)


@shared_task
def on_chord_error(request, exc, traceback):
    # TODO: remove failed keyspace computation
    logger.error("Task {0!r} raised error: {1!r}".format(request.id, exc))
