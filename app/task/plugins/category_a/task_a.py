
from task.plugins.base_task import BaseTask
from task.common.logger import get_logger
from task.common.utils import SERVICE_NAME
logger = get_logger(SERVICE_NAME)

class TaskA(BaseTask):
    def do_perform(self, args : list):
        logger.info(f'Task A is running. args: {args}')
        self.result_message["message"] = "Task A is done"
        return_value = ""
        for v in args:
            return_value += v + " "
        self.result_message["data"]['return_value'] = return_value
