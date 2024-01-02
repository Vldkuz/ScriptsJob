from GitWorker import GitWorker


class GitManager:
    def __init__(self, url, branch):
        self.url = url
        self.branch = branch

    def __enter__(self):
        self.git = GitWorker(self.url, self.branch)
        self.git.clone()
        self.git.switch(self.branch)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.git.delete_repo()
