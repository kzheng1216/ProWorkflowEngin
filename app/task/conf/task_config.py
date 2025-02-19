from copy import deepcopy
import json
import yaml
import os

from task.common.logger import get_logger
from task.common.utils import SERVICE_NAME, ExecutionMode
logger = get_logger(SERVICE_NAME)

base_dir = os.path.dirname(os.path.abspath(__file__))
yaml_task_definition = os.path.join(base_dir, '', 'task_definition.yaml')
profile_dir = f'{base_dir}/profile/'


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class TaskConfig:
    config = {}

    def __init__(self):
        self.load_conf()

    def load_conf(self):
        # Load task definition
        with open(yaml_task_definition, 'r') as f:
            task_definition_data = yaml.safe_load(f)
            task_dfs = task_definition_data['task_definition']
            t = {}
            for t_dfs in task_dfs:
                t[t_dfs['id']] = t_dfs
            self.config['Task'] = t

        # Load profile
        self.config['Profile'] = {}
        for item in os.listdir(profile_dir):
            item_path = os.path.join(profile_dir, item)
            if os.path.isfile(item_path):
                with open(item_path, 'r') as f:
                    profile_data = yaml.safe_load(f)
                    self.config['Profile'][profile_data['profile']] = profile_data

        logger.info(f'Load task config: {json.dumps(self.config, indent=4)}')
    
    def get_task_definitions_by_profile_name(self, profile_name: str) -> list:
        task_definitions = []
        profile_inst = self.config['Profile'][profile_name]
        if not profile_inst or not profile_inst['plugins']:
            return []
        for plugin in profile_inst['plugins']:
            task_definitions.append(self.config['Task'][plugin])
        return task_definitions

    def get_execution_mode_by_profile_name(self, profile_name: str) -> ExecutionMode:
        profile_inst = self.config['Profile'][profile_name]   
        if not profile_inst or not profile_inst['execution-mode'] or profile_inst['execution-mode'] == ExecutionMode.SEQUENTIAL.value:
            return ExecutionMode.SEQUENTIAL
        return ExecutionMode.PARALLEL

if __name__ == "__main__":
    m = TaskConfig()
    k = m.get_task_definitions_by_profile_name('plan_01a')
    print(k)
