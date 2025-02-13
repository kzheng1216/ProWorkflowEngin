import yaml
import os

current_dir = os.path.dirname(__file__)
yaml_file_path = os.path.join(current_dir, '', 'task_definition.yaml') 


class TaskDefinition:
    task_map = {}  
    def __init__(self):
        self.load_task_definition()

    def load_task_definition(self):
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)
            self.task_map = config['task_definition']
   