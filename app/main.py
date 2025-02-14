import json
from task.common.utils import SERVICE_NAME
from task.common.logger import get_logger
from task.execute.plan import Plan
from task.execute.executor import TaskExecutor
    
logger = get_logger(SERVICE_NAME)

# 主函数
if __name__ == "__main__":
    plan = Plan('profile_01a')
    executor = TaskExecutor(plan)
    executor.executor()
    logger.info(json.dumps(plan.get_result(), indent=4))
 