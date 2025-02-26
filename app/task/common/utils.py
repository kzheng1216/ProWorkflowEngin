from enum import Enum
import os

SERVICE_NAME = "TaskService"

# LOG
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
