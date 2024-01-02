import os
import shutil
import subprocess

from WebWorker import WebWorker


class GitWorker:
    def __init__(self, url_repo, branch):
        if WebWorker.check_ref(url_repo):
            self.url_repo = url_repo
            self.branch = branch
            self.dir = url_repo[url_repo.rfind('/') + 1: url_repo.rfind('.')]
        else:
            raise Exception('Invalid url repo')

    def clone(self):
        clone = subprocess.run(['git', 'clone', self.url_repo])
        if not GitWorker.command_checker(clone):
            raise Exception(clone.stdout)
        os.chdir(self.dir)

    def switch(self, branch):
        switch = subprocess.run(['git', 'switch', branch])
        if not GitWorker.command_checker(switch):
            raise Exception(switch.stdout)
        self.branch = branch

    def delete_repo(self):
        os.chdir('..')
        shutil.rmtree(self.dir)

    def create(self, branch):
        create = subprocess.run(['git', 'switch -с', branch])
        if not GitWorker.command_checker(create):
            raise Exception(create.stdout)
        self.branch = branch

    @staticmethod
    def delete(branch, local=True):
        if local:
            delete = subprocess.run(['git', 'branch -D', branch])
        else:
            delete = subprocess.run(['git', 'push', 'origin', '-d', branch])
        if not GitWorker.command_checker(delete):
            raise Exception(delete.stdout)

    def change_url(self, url):
        if WebWorker.check_ref(url):
            self.url_repo = url
        else:
            raise Exception("Invalid URL")

    @staticmethod
    def command_checker(command):
        return command.returncode == 0
