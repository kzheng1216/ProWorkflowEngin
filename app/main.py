import json
from task.execute.executor import Executor
from task.common.utils import SERVICE_NAME
from task.common.logger import get_logger

logger = get_logger(SERVICE_NAME)

# 主函数
if __name__ == "__main__":
    executor = Executor('profile_01a')
    executor.run()
    logger.info(f'Result Message:  {json.dumps(executor.get_result(), indent=4)}')
 