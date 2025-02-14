from copy import deepcopy
import json
import yaml
import importlib
import os
from task.execute.plan import Plan
from task.conf.task_config import TaskConfig

    
class TaskExecutor:
    config = TaskConfig()
    plan = Plan()
    
    def __init__(self, plan : Plan):
        self.plan = plan

    def executor(self):
        task_dfs = self.config.get_task_definitions_by_profile_name(self.plan.profile)
        task_result = deepcopy(task_dfs)

        for t in task_result:
            module_name = t['command']

            # Load class
            module_name = module_name.replace('/', '.').replace('.py', '')
            task_module = importlib.import_module(
                f'task.plugins.{module_name}')
            task_class = getattr(task_module, t['id'])

            # create instance
            task_instance = task_class()

            # call method
            method = getattr(task_instance, 'perform')
            method()
            t['result_message'] = task_instance.result_message
            
        self.plan.result(task_result)
