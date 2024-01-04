import datetime
import os
import shutil


class DirectoryManager:
    def __init__(self):
        self.name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def __enter__(self):
        os.makedirs(self.name, exist_ok=True)
        os.chdir(self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir('..')
        shutil.rmtree(self.name)
