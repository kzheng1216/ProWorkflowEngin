from enum import Enum
import os

SERVICE_NAME = "TaskService"

# Config file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YAML_TASK_DEFINITION = os.path.join(BASE_DIR, '../conf/', 'task_definition.yaml')
PROFILE_DIR = f'{BASE_DIR}/../conf/profile/'


# Log config
LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'INFO')
LOGGING_FORMAT = '%(asctime)s [%(levelname)s] <%(threadName)s:%(thread)d> %(filename)s %(funcName)s() (%(lineno)d): %(message)s'



class State(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    ERROR = "ERROR"


class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

