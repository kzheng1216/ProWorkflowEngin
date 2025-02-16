import asyncio
from copy import deepcopy
import json
import yaml
import importlib
from task.conf.task_config import TaskConfig
from task.common.utils import State
from task.common.utils import SERVICE_NAME, ExecutionMode
from task.common.logger import get_logger

logger = get_logger(SERVICE_NAME)


class BaseExecutor:
    config = TaskConfig()
    profile = 'default'
    task_list = []
    execution_mode = ExecutionMode.SEQUENTIAL

    total_result_message = {
        "status": State.NEW.value,
        "tasks": [],
    }

    def __init__(self, profile : str = 'default'):
        self.profile = profile
        self.task_list = self.config.get_task_definitions_by_profile_name(self.profile)
        self.execution_mode = self.config.get_execution_mode_by_profile_name(self.profile)

    def executor_module(self, task_data: dict) -> dict:
        module_name = task_data["command"]

        # Load class
        module_name = module_name.replace("/", ".").replace(".py", "")
        task_module = importlib.import_module(f"task.plugins.{module_name}")
        task_class = getattr(task_module, task_data["id"])

        # create instance
        task_instance = task_class()

        # call method
        method = getattr(task_instance, "perform")
        method()
        return task_instance.result_message
    
    def result(self):
        if not self.task_list:
            self.result_message['status'] = State.ERROR.value
            return

        self.total_result_message['tasks'] = self.task_list
        
        for task in self.task_list:    
            if task['result_message']['status'] == State.FAIL.value:
                self.total_result_message['status'] = State.FAIL.value
                return

            if task['result_message']['status'] == State.ERROR.value:
                self.total_result_message['status'] = State.ERROR.value
                return
        self.total_result_message['status'] = State.SUCCESS.value
            
    def get_result(self):
        return self.total_result_message
