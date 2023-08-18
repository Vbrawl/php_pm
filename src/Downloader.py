from git.repo import Repo as GitRepo
from git.remote import RemoteProgress
from sys import stdout
from utils import parts_in_path
from os.path import join as PathJoin

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
    
    def download_from_git(self, url):
        fname = parts_in_path(url)[-1]
        if fname.endswith('.git'):
            fname = fname[:-4]
        GitRepo.clone_from(url, PathJoin(self.path, fname), DownloadProgress()) # type: ignore
