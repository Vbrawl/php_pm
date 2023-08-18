from Project import *
from Config import *
import os
import argparse

config = Config()



class Main():
    def __init__(self, config):
        self.config = config
        self.PROJECT_LIBRARY = ProjectLibrary(config.library_path)

    def initialize_project(self):
        proj = Project(os.getcwd())
        projJs = os.path.join(proj.path, proj.project_json_filename)
        if not os.path.isfile(projJs):
            proj.save(projJs)
        projLibrary = os.path.join(proj.path, proj.library_directory)
        if not os.path.isdir(projLibrary):
            proj.clear_library_folder()
        projRelocation = os.path.join(proj.path, proj.relocation_config)
        if not os.path.isfile(projRelocation):
            proj.add_root_relocation()


if __name__ == "__main__":
    m = Main(config)

    ACTIONS = {
        "init": m.initialize_project,
    }


    parser = argparse.ArgumentParser(app_name)
    parser.add_argument("action", action="store", help="Available Actions: " + ', '.join(ACTIONS.keys()))

    args = parser.parse_args()



    action:str = args.action
    if action in ACTIONS:
        ACTIONS[action]()