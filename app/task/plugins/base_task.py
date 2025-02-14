from task.common.utils import State
from task.common.logger import get_logger
from task.common.utils import SERVICE_NAME
logger = get_logger(SERVICE_NAME)

    
class BaseTask:
    result_message = {
        "status": State.READY.value,
        "message": ""
    }

    def perform(self):
        try:         
            self.result_message["status"] = State.RUNNING.value
            self.do_perform()
            self.result_message["status"] = State.SUCCESS.value
        except Exception as e:
            self.result_message["status"] = State.ERROR.value
            self.result_message["message"] = str(e)
            
    def do_perform(self):
        logger.info("Base Task is running")
