import asyncio
from copy import deepcopy
import json
import yaml
import importlib
import os
from task.execute.plan import Plan
from task.conf.task_config import TaskConfig
from task.common.utils import SERVICE_NAME, ExecutionMode
from task.common.logger import get_logger

logger = get_logger(SERVICE_NAME)


class TaskExecutor:
    config = TaskConfig()
    plan = Plan()

    def __init__(self, plan: Plan):
        self.plan = plan

    def executor(self):
        task_dfs = self.config.get_task_definitions_by_profile_name(
            self.plan.profile)
        execution_mode = self.config.get_execution_mode_by_profile_name(
            self.plan.profile)
        logger.info(f'execution_mode: {execution_mode.value}')
        task_result = deepcopy(task_dfs)
        if execution_mode == ExecutionMode.SEQUENTIAL:
            task_result = self.executor_sequential(task_result)
        else:
            task_result = self.executor_parallel(task_result)
        self.plan.result(task_result)

    def executor_sequential(self, task_result: list) -> list:
        for t in task_result:
            t['result_message'] = self.executor_module(t)
        return task_result

    async def executor_parallel(self, task_result: list):
        parallel_tasks = [self.executor_module_async(t) for t in task_result]
        result_messages = await asyncio.gather(*parallel_tasks)
        print(result_messages)
        return task_result

    async def executor_module_async(self, task_data: dict) -> dict:
        return self.executor_module(task_data)
    
    def executor_module(self, task_data: dict) -> dict:
        module_name = task_data['command']

        # Load class
        module_name = module_name.replace('/', '.').replace('.py', '')
        task_module = importlib.import_module(f'task.plugins.{module_name}')
        task_class = getattr(task_module, task_data['id'])

        # create instance
        task_instance = task_class()

        # call method
        method = getattr(task_instance, 'perform')
        method()
        return task_instance.result_message
