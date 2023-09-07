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
        self.PROJECT_LIBRARY = ProjectLibrary(config.library_path, config.database_path)
        self.DOWNLOADER = Downloader(config.download_path)

    def initialize_project(self):
        proj = Project(os.getcwd())
        projJs = os.path.join(proj.path, proj.project_json_filename)
        if not os.path.isfile(projJs):
            proj.save(projJs)
        
        resource_folder = os.path.join(proj.path, proj.input_resource_directory)
        if not os.path.isdir(resource_folder):
            os.makedirs(resource_folder)
    
    def register_project(self):
        proj = Project(os.getcwd())
        if self.PROJECT_LIBRARY.get_project(proj.name):
            raise Exception("A project with this name is already registered.")
        else:
            self.PROJECT_LIBRARY.add_project_link(proj)

    def deregister_project(self, project_name:str):
        if project_name is None:
            raise Exception("A project name is required.")
        proj = self.PROJECT_LIBRARY.get_project(project_name)
        if proj:
            self.PROJECT_LIBRARY.remove_project(project_name)
        else:
            raise Exception("No project is registered with this name.")
    
    def list_projects(self):
        for project_line in map(lambda x: f'{x.name} : {x.url} : {x.version} : {x.path}', self.PROJECT_LIBRARY.list_projects()):
            print(project_line)
    
    def add_project(self, project_name:str):
        root_prj = Project(os.getcwd())
        proj = self.PROJECT_LIBRARY.get_project(project_name)

        if proj:
            root_prj.register_project(proj)
            root_prj.save(root_prj.project_json_filename)
        else:
            raise Exception("No project is registered with this name.")
    
    def remove_project(self, project_name:str):
        root_prj = Project(os.getcwd())
        root_prj.deregister_project(project_name)
        root_prj.save(root_prj.project_json_filename)
    
    def resolve_requirements(self):
        root_project = Project(os.getcwd())

        if os.path.exists(os.path.join(root_project.path, root_project.project_json_filename)):
            root_project.clear_library_folder()
            root_project.clear_resource_folder()

            all_projects = [root_project]

            while all_projects != []:
                requirement_project = all_projects.pop()
                for name, url in requirement_project.requirements.items():
                    proj = self.PROJECT_LIBRARY.get_project(name)

                    if not proj and url != '':
                        self.download_project(url)
                        proj = self.PROJECT_LIBRARY.get_project(name)

                    if proj:
                        root_project.import_project(proj)
                        all_projects.append(proj)
            root_project.add_root_relocation()
        else:
            raise Exception("This is not a project directory. Run the 'init' command.")
    
    def download_project(self, project_url:str):
        tmp = self.DOWNLOADER.download_from_git(project_url)
        if os.path.isfile(os.path.join(tmp, "project.json")):
            proj = Project(tmp)
            self.PROJECT_LIBRARY.add_project(proj)

    def clear_project(self):
        prj = Project(os.getcwd())

        if os.path.exists(os.path.join(prj.path, prj.project_json_filename)):

            library_path = os.path.join(prj.path, prj.library_directory)
            libexists = os.path.isdir(library_path)
            reloc_path = os.path.join(prj.path, prj.relocation_config)
            relocexists = os.path.isfile(reloc_path)
            jsreloc_path = os.path.join(prj.path, prj.javascript_relocation_config)
            jsrelocexists = os.path.isfile(jsreloc_path)
            res_path = os.path.join(prj.path, prj.output_resource_directory)
            resexists = os.path.isdir(res_path)

            if not libexists and not relocexists and not resexists and not jsrelocexists:
                raise Exception("Project directory is already clean.")
            else:
                if libexists:
                    utils.delete_folder(library_path)
                if res_path:
                    utils.delete_folder(res_path)
                if relocexists:
                    os.unlink(reloc_path)
                if jsrelocexists:
                    os.unlink(jsreloc_path)
        else:
            raise Exception("This is not a project directory. Run the 'init' command.")




if __name__ == "__main__":
    m = Main(config)

    ACTIONS = {
        "init": {"args": (), "func": m.initialize_project},
        "register": {"args": (), "func": m.register_project},
        "deregister": {"args": ("project_name",), "func": m.deregister_project},
        "list": {"args": (), "func": m.list_projects},
        "add": {"args": ("project_name",), "func": m.add_project},
        "remove": {"args": ("project_name",), "func": m.remove_project},
        "resolve": {"args": (), "func": m.resolve_requirements},
        "download": {"args": ("project_url",), "func": m.download_project},
        "clear": {"args": (), "func": m.clear_project}
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
