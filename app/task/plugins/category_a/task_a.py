
from task.plugins.base_task import BaseTask
from task.common.logger import get_logger
from task.common.utils import SERVICE_NAME
logger = get_logger(SERVICE_NAME)

class TaskA(BaseTask):
    def do_perform(self):
        logger.info("Task A is running")
        self.result_message["message"] = "Task A is done"
