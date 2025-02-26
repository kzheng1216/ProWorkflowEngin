import asyncio
from copy import deepcopy
import json
import yaml
import importlib
from task.execute.task_config import TaskConfig
from task.common.utils import State
from task.common.utils import SERVICE_NAME, ExecutionMode
from task.common.logger import get_logger

logger = get_logger(SERVICE_NAME)


class Executor:
    config = TaskConfig()
    tasks = []
    mode = ExecutionMode.SEQUENTIAL

    total_result_message = {
        "status": State.NEW.value,
        "tasks": [],
    }

    def __init__(self, profile_name : str = 'default'):
        self.tasks = self.config.get_tasks(profile_name)
        self.mode = self.config.get_execution_mode(profile_name)
        logger.info(
            f"### === [Profile]: {profile_name} | [Execution Mode]: {self.mode.value}")

    
    def execute_task(self, task_data: dict) -> dict:
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
    
    def handle_result(self):
        if not self.tasks:
            self.result_message['status'] = State.ERROR.value
            return

        self.total_result_message['tasks'] = self.tasks
        
        for task in self.tasks:
            if task['result_message']['status'] == State.FAIL.value:
                self.total_result_message['status'] = State.FAIL.value
                return

            if task['result_message']['status'] == State.ERROR.value:
                self.total_result_message['status'] = State.ERROR.value
                return
        self.total_result_message['status'] = State.SUCCESS.value
            
    def get_result(self):
        return self.total_result_message

    def run_parallel(self):
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.executor_module_async(t))
                 for t in self.tasks]

        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            logger.error(f"executor_parallel error: {e}")
        loop.close()

        self.tasks = [task.result() for task in tasks]
        self.handle_result()

    async def executor_module_async(self, task_data: dict) -> dict:
        task_data["result_message"] = self.execute_task(task_data)
        return task_data

    def run_sequential(self):
        for t in self.tasks:
            t["result_message"] = self.execute_task(t)
        self.handle_result()

    def run(self):
        try:
            if self.mode == ExecutionMode.PARALLEL:
                self.run_parallel()
            else:
                self.run_sequential()
        except Exception as e:
            logger.error(f"Error occur during execution: {e}")
