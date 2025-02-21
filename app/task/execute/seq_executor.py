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


class SeqExecutor(BaseExecutor):
    def run_seq(self):
        for t in self.task_list:
            t["result_message"] = self.executor_module(t)
 