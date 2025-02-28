from copy import deepcopy
import json
import yaml
import os
from task.common.logger import get_logger
from task.common.utils import PROFILE_DIR, SERVICE_NAME, YAML_TASK_DEFINITION, ExecutionMode, singleton
logger = get_logger(SERVICE_NAME)


@singleton
class TaskConfig:
    def __init__(self):
        self.config = {}
        self.load_conf()

    def load_conf(self):
        try:
            # Load task definition
            with open(YAML_TASK_DEFINITION, 'r') as f:
                data = yaml.safe_load(f)
                if data.__contains__('task_definition'):
                    self.config['Task'] = {t_dfs['id']: t_dfs for t_dfs in data['task_definition']}
                else:
                    self.config['Task'] = {}

            # Load profile
            self.config['Profile'] = {}
            for item in os.listdir(PROFILE_DIR):
                item_path = os.path.join(PROFILE_DIR, item)
                if not os.path.isfile(item_path):
                    continue
                with open(item_path, 'r') as f:
                    data = yaml.safe_load(f)
                    self.config['Profile'][data['profile']] = data
                        
        except Exception as e:
            logger.error(f'Load task config failed: {e}')

        logger.info(f'Load task config: {json.dumps(self.config, indent=4)}')
    
    def get_tasks(self, profile_name: str) -> list:
        task_definitions = []
        if not self.config['Profile'].__contains__(profile_name):
            return []
        
        profile_inst = self.config['Profile'][profile_name]
        if not profile_inst or not profile_inst['plugins']:
            return []
        for plugin in profile_inst['plugins']:
            task_definitions.append(self.config['Task'][plugin])
        return task_definitions

    def get_execution_mode(self, profile_name: str) -> ExecutionMode:
        profile_inst = self.config['Profile'][profile_name]   
        if not profile_inst \
            or not profile_inst['execution-mode'] \
            or profile_inst['execution-mode'] == ExecutionMode.SEQUENTIAL.value:
            return ExecutionMode.SEQUENTIAL
        return ExecutionMode.PARALLEL

if __name__ == "__main__":
    m = TaskConfig()
    k = m.get_task_definitions_by_profile_name('plan_01a')
    print(k)
