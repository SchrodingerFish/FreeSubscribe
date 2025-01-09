import threading
import time

from Scheduled.sync_md import GitHubMDUploader
from config.log_config import logger

class TaskScheduler:
    def __init__(self, interval=15):
        self.interval = interval
        self.lock = threading.Lock()
        self.uploader = GitHubMDUploader()

    def run_task(self):
        if self.lock.acquire(blocking=False):
            try:
                self.uploader.process()
            finally:
                threading.Timer(self.interval, self.run_task).start()
                self.lock.release()
        else:
            logger.info("Task is still running, skipping this interval...")

if __name__ == '__main__':
    scheduler = TaskScheduler(interval=21600)
    logger.info("File upload scheduler start...")
    scheduler.run_task()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.exception("The program is interrupted by key board...")
