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
        logger.info(f'---------------------------------------------------------')
        task_id = task_data["id"]
        logger.info(f'--- [Execute Task]: {task_id}')
        # logger.info(f'task_data: {json.dumps(task_data, indent=4)}')
        module_name = task_data["command"]
        args_data = task_data["args"]

        # Load class
        module_name = module_name.replace("/", ".").replace(".py", "")
        task_module = importlib.import_module(f"task.plugins.{module_name}")
        task_class = getattr(task_module, task_data["id"])
        logger.info(f'--- [Task Class]: {task_class}')

        # create instance
        task_instance = task_class()

        # # call method
        method = getattr(task_instance, "perform")
        method(args_data)
        result_message = deepcopy(task_instance.result_message)
        
        logger.info(f'[Result Message]: {json.dumps(result_message, indent=4)}')
        return result_message
    
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
