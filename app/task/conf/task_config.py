import json
import yaml
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
yaml_task_definition = os.path.join(base_dir, '', 'task_definition.yaml') 
profile_dir = f'{base_dir}/profile/'

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
        for item in os.listdir(profile_dir):
            item_path = os.path.join(profile_dir, item)
            if os.path.isfile(item_path):
                print(item_path)
                with open(item_path, 'r') as f:
                    profile_data = yaml.safe_load(f)
                    self.config['Profile'] = {
                        profile_data['profile']: profile_data
                    }
            

        print(json.dumps(self.config, indent=4))


if __name__ == "__main__":
    m = TaskConfig()
 