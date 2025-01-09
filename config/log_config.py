import sys
from pathlib import Path
from loguru import logger


def setup_logger():
    # 移除默认的控制台输出处理器
    logger.remove()

    # 获取项目根目录（假设log_config.py在项目根目录的某个子目录中）
    root_path = Path(__file__).parent.parent
    log_path = root_path / 'logs'

    # 确保日志目录存在
    log_path.mkdir(parents=True, exist_ok=True)

    # 构建完整的日志文件路径
    log_file = log_path / "free_subcribe.log"

    # 添加文件处理器
    logger.add(
        str(log_file),
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
        enqueue=True
    )

    # 添加控制台输出
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
    )

    return logger


# 初始化logger
logger = setup_logger()