import logging
import os
from task.common.utils import LOGGING_LEVEL, LOGGING_FORMAT


def get_logger(name):
    # 检查 logs 目录是否存在，如果不存在则创建
    current_file_path = os.path.abspath(__file__).replace('logger.py', '../../..')
    log_dir = f'{current_file_path}/logs'
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 配置日志记录器
    log_file = os.path.join(log_dir, 'app.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 创建日志记录器实例
    logger = logging.getLogger(name)
    return logger

