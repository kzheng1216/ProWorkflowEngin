
from task.plugins.base_task import BaseTask
from task.common.logger import get_logger
from task.common.utils import SERVICE_NAME
logger = get_logger(SERVICE_NAME)

class TaskB(BaseTask):
    def do_perform(self, args: list):
        logger.info(f'Task B is running. args: {args}')
        self.result_message["message"] = "Task B is done"
        self.result_message["data"]['return_value'] = "234"
