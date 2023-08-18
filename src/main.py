from Project import ProjectLibrary, Project
from Config import Config, app_name
from Downloader import Downloader
import os
import argparse
import utils

config = Config()



class Main():
    def __init__(self, config):
        self.config = config
        self.PROJECT_LIBRARY = ProjectLibrary(config.library_path)
        self.DOWNLOADER = Downloader(config.download_path)

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
    
    def register_project(self):
        proj = Project(os.getcwd())
        if self.PROJECT_LIBRARY.get_project(proj.name):
            raise Exception("A project with this name is already registered.")
        else:
            self.PROJECT_LIBRARY.add_project(proj)

    def deregister_project(self, project_name:str):
        if project_name is None:
            raise Exception("A project name is required.")
        # print(project_name)
        proj = self.PROJECT_LIBRARY.get_project(project_name)
        if proj:
            self.PROJECT_LIBRARY.remove_project(project_name)
        else:
            raise Exception("No project is registered with this name.")
    
    def list_projects(self):
        for project_line in map(lambda x: f'{x.name} : {x.url} : {x.version}', self.PROJECT_LIBRARY.projects):
            print(project_line)
    
    def add_project(self, project_name:str):
        root_prj = Project(os.getcwd())
        proj = self.PROJECT_LIBRARY.get_project(project_name)

        if proj:
            root_prj.register_project(proj)
            root_prj.save(root_prj.project_json_filename)
        else:
            raise Exception("No project is registered with this name.")
    
    def resolve_requirements(self):
        prj = Project(os.getcwd())

        prj.clear_library_folder()

        for name, url in prj.requirements.items():
            proj = self.PROJECT_LIBRARY.get_project(name)

            if proj:
                prj.import_project(proj)
        prj.add_root_relocation()
    
    def download_project(self, project_url:str):
        tmp = self.DOWNLOADER.download_from_git(project_url)
        if os.path.isfile(os.path.join(tmp, "project.json")):
            proj = Project(tmp)
            self.PROJECT_LIBRARY.add_project(proj)




if __name__ == "__main__":
    m = Main(config)

    ACTIONS = {
        "init": {"args": (), "func": m.initialize_project},
        "register": {"args": (), "func": m.register_project},
        "deregister": {"args": ("project_name",), "func": m.deregister_project},
        "list": {"args": (), "func": m.list_projects},
        "add": {"args": ("project_name",), "func": m.add_project},
        "resolve": {"args": (), "func": m.resolve_requirements},
        "download": {"args": ("project_url",), "func": m.download_project}
    }


    parser = argparse.ArgumentParser(app_name)
    parser.add_argument("action", action="store", help="Available Actions: " + ', '.join(ACTIONS.keys()))
    parser.add_argument("-pn", "--project-name", action="store", help="The project name.", required=False)
    parser.add_argument("-pu", "--project-url", action="store", help="The project URL.")
    args = parser.parse_args()


    action:str = args.action
    if action in ACTIONS:
        action_data = ACTIONS[action]
        arguments = []
        for argname in action_data["args"]:
            if argname in args.__dict__:
                arguments.append(args.__dict__[argname])
        action_data["func"](*arguments)