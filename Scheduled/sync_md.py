import json
from pprint import pprint

import paramiko
import os
import requests
from datetime import datetime
import shutil
import tempfile
import dotenv

from config.log_config import logger

dotenv.load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_BRANCH = os.getenv('GITHUB_BRANCH')
GITHUB_MD_PATH = os.getenv('GITHUB_MD_PATH')

SSH_HOST = os.getenv('SSH_HOST')
SSH_PORT = os.getenv('SSH_PORT')
SSH_USERNAME = os.getenv('SSH_USERNAME')
SSH_PASSWORD = os.getenv('SSH_PASSWORD')
REMOTE_DIR = os.getenv('REMOTE_DIR')


class GitHubMDUploader:
    def __init__(self):
        self.github_headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.temp_dir = None

    def create_temp_dir(self):
        self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir

    def cleanup_temp_dir(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def get_github_files(self):
        try:
            url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_MD_PATH}'
            response = requests.get(url, headers=self.github_headers, params={'ref': GITHUB_BRANCH})
            response.raise_for_status()
            logger.info(f"Successfully fetched files from GitHub")
            return response.json()
        except Exception as e:
            logger.exception(f"Error fetching files from GitHub: {str(e)}")
            return []

    def download_file(self, file_info):
        try:
            if file_info["type"] == 'file' and (file_info["name"].endswith('.md') or file_info["name"].endswith('.html')):
                response = requests.get(file_info["download_url"], headers=self.github_headers)
                response.raise_for_status()
                local_path = os.path.join(self.temp_dir, file_info["name"])
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                    logger.info(f"Successfully downloaded {file_info['name']}")
                return local_path
        except Exception as e:
            logger.exception(f"Error downloading file {file_info["name"]}: {str(e)}")
        return None

    def upload_to_ssh(self, local_file):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(SSH_HOST, int(SSH_PORT), SSH_USERNAME, SSH_PASSWORD)
            sftp = ssh.open_sftp()

            if local_file and os.path.exists(local_file):
                logger.info("The local_file: "+local_file)
                filename = os.path.basename(local_file)
                logger.info("The filename: "+filename)
                remote_path = REMOTE_DIR+"/"+filename
                logger.info("The remote_path: "+remote_path)
                sftp.put(local_file, remote_path)
                logger.info(f"Successfully uploaded {filename}")

            sftp.close()
            ssh.close()

        except Exception as e:
            logger.exception(f"Error in SSH upload: {str(e)}")

    def process(self):
        try:
            logger.info(f"Starting process...")

            self.create_temp_dir()

            files = self.get_github_files()
            if not files:
                return
            else:
                for file in files:
                    if file["name"].endswith('.md') or file["name"].endswith('.html'):
                        logger.info(f"Found file in GitHub: \n")
                        if isinstance(file, str):
                            data = json.loads(file)
                        else:
                            data = file

                        pprint(data)
                        local_path = self.download_file(file)

                        if local_path:
                            self.upload_to_ssh(local_path)

        except Exception as e:
            logger.exception(f"Error in process: {str(e)}")
        finally:
            self.cleanup_temp_dir()
            logger.info(f"Process completed.")

