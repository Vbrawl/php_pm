from git.repo import Repo as GitRepo
from git.remote import RemoteProgress
from sys import stdout
import tempfile
import os

class DownloadProgress(RemoteProgress):
    def update(self, *args, **kwargs):
        if self._cur_line:
            stdout.write(self._cur_line)
            if self._cur_line.endswith(self.DONE_TOKEN):
                stdout.write("\n")
            else:
                stdout.write("\r")



class Downloader:
    def __init__(self, path:str):
        self.path = path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
    
    def download_from_git(self, url):
        tempdir = tempfile.mkdtemp("git", "download", self.path)
        GitRepo.clone_from(url, tempdir, DownloadProgress()) # type: ignore
        return tempdir