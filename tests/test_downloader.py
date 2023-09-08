import unittest
import json
import os, sys, tempfile

if 'src' not in sys.path:
    sys.path.append("src")
if '../src' not in sys.path:
    sys.path.append("../src")

import Downloader
class Test_Downloader(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.dir = tempfile.mkdtemp("downloader")
        super().__init__(*args, **kwargs)

    def test_download_from_git(self):
        url = "https://github.com/vbrawl/php_pm.git"
        downloader = Downloader.Downloader(self.dir)
        tempdir = downloader.download_from_git(url)

        self.assertTrue(os.path.isdir(tempdir), "Project was not downloaded correctly.")

if __name__ == "__main__":
    unittest.main()