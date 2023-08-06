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

class Project:
    def __init__(self, path:str, project_json_filename:str = "project.json"):
        self.path = path
        self.project_json_filename = project_json_filename
        self.config = ProjectJson(os.path.join(path, project_json_filename))
    
    def import_project(self, project: 'Project'):
        dest = os.path.join(self.path, self.config.library_directory, project.config.name)
        utils.copy_tree(project.path, dest)
    
    def clear_library_folder(self):
        lib_folder = os.path.join(self.path, self.config.library_directory)
        if os.path.isdir(lib_folder): utils.delete_folder(lib_folder)
        os.mkdir(lib_folder)