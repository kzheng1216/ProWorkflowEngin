import asyncio
from copy import deepcopy
import json
import yaml
import importlib
from task.execute.parallel_executor import ParallelExecutor
from task.execute.seq_executor import SeqExecutor
from task.execute.base_executor import BaseExecutor
from task.common.utils import State
from task.common.utils import SERVICE_NAME, ExecutionMode
from task.common.logger import get_logger

logger = get_logger(SERVICE_NAME)


class TaskExecutor(ParallelExecutor, SeqExecutor):
    def run(self):
        logger.info(f"### === [Profile]: {self.profile} | [Execution Mode]: {self.execution_mode.value}")
        if self.execution_mode == ExecutionMode.SEQUENTIAL:
            self.run_seq()
        else:
            self.run_parallel()
        self.result()

