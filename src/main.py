from Project import *
from Config import *
import os

config = Config()



class Main():
    def __init__(self, config):
        self.config = config
        self.PROJECT_LIBRARY = ProjectLibrary(config.library_path)

    def initialize_project(self):
        proj = Project(os.getcwd())
        projJs = os.path.join(proj.path, proj.project_json_filename)
        if not os.path.exists(projJs):
            proj.save(projJs)


if __name__ == "__main__":
    m = Main(config)
    m.initialize_project()
