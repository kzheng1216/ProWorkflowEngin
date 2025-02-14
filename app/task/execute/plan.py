from enum import Enum
from task.common.utils import State
    
class Plan:
    total_result_message = {
        "status": State.NEW.value,
        "tasks": [],
    }
    profile = 'default'
       
    def __init__(self, profile : str = 'default'):
        self.profile = profile
    
    def result(self, task_result : list):
        if not task_result:
            self.result_message['status'] = State.ERROR.value
            return

        self.total_result_message['tasks'] = task_result
        
        for task in task_result:    
            if task['result_message']['status'] == State.FAIL.value:
                self.total_result_message['status'] = State.FAIL.value
                return

            if task['result_message']['status'] == State.ERROR.value:
                self.total_result_message['status'] = State.ERROR.value
                return
        self.total_result_message['status'] = State.SUCCESS.value
            
    def get_result(self):
        return self.total_result_message
