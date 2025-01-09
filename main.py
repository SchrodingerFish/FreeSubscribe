import threading
import time
from datetime import datetime

from Scheduled.sync_md import GitHubMDUploader
from config.log_config import logger

class TaskScheduler:
    def __init__(self, interval=15):
        self.interval = interval
        self.lock = threading.Lock()  # 用于控制任务是否可以执行
        self.uploader = GitHubMDUploader()

    def run_task(self):
        if self.lock.acquire(blocking=False):  # 尝试获取锁
            try:
                self.uploader.process()  # 执行任务
            finally:
                # 设置下一次任务
                threading.Timer(self.interval, self.run_task).start()
                self.lock.release()  # 释放锁
        else:
            logger.info("Task is still running, skipping this interval...")

if __name__ == '__main__':
    scheduler = TaskScheduler(interval=21600)

    logger.info("File upload scheduler start...")

    # 启动定时任务
    scheduler.run_task()

    # 让主线程保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.exception("The program is interrupted by key board...")
