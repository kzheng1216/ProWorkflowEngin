import asyncio
from copy import deepcopy
import json
import yaml
import importlib
from task.execute.base_executor import BaseExecutor
from task.common.utils import State
from task.common.utils import SERVICE_NAME, ExecutionMode
from task.common.logger import get_logger

logger = get_logger(SERVICE_NAME)


class ParallelExecutor(BaseExecutor):
    def run_parallel(self):
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.executor_module_async(t)) for t in self.task_list]

        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as e:
            logger.error(f"executor_parallel error: {e}")
        loop.close()

        self.task_list = [task.result() for task in tasks]
    
    async def executor_module_async(self, task_data: dict) -> dict:
        task_data["result_message"] = self.executor_module(task_data)
        return task_data
    

