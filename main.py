import time

import schedule

from Scheduled.sync_md import GitHubMDUploader

if __name__ == '__main__':
    uploader = GitHubMDUploader()

    # 设置定时任务，每天特定时间执行
    schedule.every().day.at("10:00").do(uploader.process)

    print("File upload scheduler started...")

    # 运行定时任务
    while True:
        schedule.run_pending()
        time.sleep(60)