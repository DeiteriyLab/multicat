import logging

from celery import current_task, shared_task
from config import Config, Database
from hashcat import FileManager, HashcatBruteforce, HashcatKeyspace, HashcatBenchmark
from hashcat.hashcat import Hashcat
from schemas import HashcatDiscreteTask

logger = logging.getLogger(__name__)
db = Database(Config.get("DATABASE_URL"))
file_manager = FileManager(Config.get("RULES_DIR"), Config.get("WORDLISTS_DIR"))
hashcat = Hashcat()
hashcat_bruteforce = HashcatBruteforce(file_manager, hashcat)
hashcat_keyspace = HashcatKeyspace(file_manager, hashcat)
hashcat_benchmark = HashcatBenchmark(file_manager, hashcat)


@shared_task(name="client.run_hashcat", ignore_result=True)
def run_hashcat(discrete_task_as_dict):
    discrete_task = HashcatDiscreteTask(**discrete_task_as_dict)
    worker_id = current_task.request.hostname
    wordlists = file_manager.get_wordlists_files()
    rules = file_manager.get_rules_files()

    success = hashcat_bruteforce.bruteforce(discrete_task)

    ...


@shared_task(name="client.calc_keyspace", ignore_result=False)
def calc_keyspace(keyspace_task):
    return hashcat_keyspace.calc_keyspace(keyspace_task)


@shared_task(name="b.benchmark", ignore_result=True)
def benchmark(hash_modes=None):
    results = hashcat_benchmark.benchmark(hash_modes)

    # TODO: write results to the backend

    ...
