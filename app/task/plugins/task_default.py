
from task.plugins.base_task import BaseTask
from task.common.logger import get_logger
from task.common.utils import SERVICE_NAME
logger = get_logger(SERVICE_NAME)

class TaskDefault(BaseTask):
    def do_perform(self):
        logger.info("Default task is running")
        self.result_message["message"] = "Default task is done"
