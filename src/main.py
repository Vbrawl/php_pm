from Project import *
from Config import *

config = Config()



class Main():
    def __init__(self, config):
        self.config = config
        self.PROJECT_LIBRARY = ProjectLibrary(config.library_path)


if __name__ == "__main__":
    m = Main(config)