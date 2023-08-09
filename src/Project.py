import os
import utils
from typing import Optional


class ProjectJson:
    def __init__(self, project_json_path:Optional[str]):
        if project_json_path and os.path.isfile(project_json_path):
            project_json = utils.read_json(project_json_path)
            if isinstance(project_json, list):
                raise TypeError("Project json file must be a key-value array.")
        else:
            project_json = {}

        get_value = lambda key, default_ = "": project_json[key] if key in project_json.keys() else default_

        self.name = get_value("project_name", "Project")
        self.version = get_value("project_version", "1.0.0")
        self.url = get_value("project_url", "")
        self.requirements = get_value("project_requirements", {})
        self.library_directory = get_value("project_library_directory", "pm_library")
        self.relocation_config = get_value("project_relocation_config", "relocation.php")
    
    def save(self, filepath):
        utils.write_json(filepath, {
            "project_name": self.name,
            "project_version": self.version,
            "project_url": self.url,
            "project_requirements": self.requirements,
            "project_library_directory": self.library_directory,
            "project_relocation_config": self.relocation_config
        })

class Project(ProjectJson):
    def __init__(self, path:str, project_json_filename:str = "project.json"):
        self.path = path
        self.project_json_filename = project_json_filename
        super().__init__(os.path.join(path, project_json_filename))
    
    def import_project(self, project: 'Project'):
        dest = os.path.join(self.path, self.library_directory, project.name)
        utils.copy_tree(project.path, dest)
    
    def clear_library_folder(self):
        lib_folder = os.path.join(self.path, self.library_directory)
        if os.path.isdir(lib_folder): utils.delete_folder(lib_folder)
        os.mkdir(lib_folder)
    
    def register_project(self, project: 'Project'):
        self.requirements[project.name] = project.url


class ProjectLibrary:
    def __init__(self, path:str):
        self.path = path
        self.projects:list[Project] = []
        if path: self.load_projects()
    
    def load_projects(self):
        self.projects = sorted(list(map(lambda x: Project(os.path.join(self.path, x)), os.listdir(self.path))), key=lambda p: p.name)