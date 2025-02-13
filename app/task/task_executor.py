import json
import yaml
import importlib
import os

from task.task_definition import TaskDefinition



class TaskExecutor:
    tasks = TaskDefinition()

    def executor(self):
        print("Task Definitions: ", json.dumps(self.tasks.task_map, indent=4))
        for t_name, t_definition in self.tasks.task_map.items():
            method_name = t_definition['method']
            module_name = f'task.category.{t_definition['category']}.{t_definition['file_name']}'
        
            # 动态加载类
            task_module = importlib.import_module(module_name) 
            task_class = getattr(task_module, t_name)
        
            # 创建类的实例
            task_instance = task_class()
        
            # 动态调用方法
            method = getattr(task_instance, method_name)
            method()
        
    