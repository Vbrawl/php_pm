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

        self.name:str = get_value("project_name", os.path.basename(os.path.dirname(project_json_path)) if project_json_path is not None else "Project")
        self.version:str = get_value("project_version", "1.0.0")
        self.url:str = get_value("project_url", "")
        self.requirements:dict[str, str] = get_value("project_requirements", {})
        self.library_directory:str = get_value("project_library_directory", "pm_library")
        self.relocation_config:str = get_value("project_relocation_config", "relocation.php")
    
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
    
    def add_root_relocation(self):
        relocation_file = os.path.join(self.path, self.relocation_config)
        utils.generate_php_config(relocation_file, definitions = {
            "PM_LIBRARY": self.library_directory
        }, sdir = True)
    
    def import_project(self, project: 'Project'):
        dest = os.path.join(self.path, self.library_directory, os.path.basename(project.path))
        utils.copy_tree(project.path, dest, exceptions=[project.library_directory, project.relocation_config])
        relocation_file = os.path.join(dest, project.relocation_config)
        main_relocation_filepath = os.path.join(self.path, self.relocation_config)

        paths = utils.remove_common_path(relocation_file, main_relocation_filepath, join = False)
        point_to_path = os.path.join('../' * len(paths[0][:-1]), *paths[1][:-1], self.relocation_config)

        utils.generate_php_config(relocation_file, requirement_files = [point_to_path])
    
    def clear_library_folder(self):
        lib_folder = os.path.join(self.path, self.library_directory)
        if os.path.isdir(lib_folder): utils.delete_folder(lib_folder)
        os.mkdir(lib_folder)
    
    def register_project(self, project: 'Project'):
        self.requirements[project.name] = project.url


class ProjectLibrary:
    def __init__(self, path:Optional[str]):
        self.path = path
        self.projects:list[Project] = []
        self.load_projects()
    
    def load_projects(self):
        if self.path is not None:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            self.projects = sorted(list(map(lambda x: Project(os.path.join(self.path, x)), os.listdir(self.path))), key=lambda p: p.name) # type: ignore
    
    def get_project(self, name:str):
        index = utils.binary_search(self.projects, name, key=lambda x: x.name)
        if index is not None:
            return self.projects[index]
    
    def add_project(self, project:Project):
        if self.path is not None:
            dest = os.path.join(self.path, os.path.basename(project.path))
            utils.copy_tree(project.path, dest, exceptions=[project.library_directory, project.relocation_config])
            project = Project(dest)
        utils.append_sorted(self.projects, project, key = lambda x: x.name)
    
    def remove_project(self, name:str):
        index = utils.binary_search(self.projects, name, key=lambda x: x.name)
        if index is not None:
            project = self.projects.pop(index)
            if self.path is not None and project.path.startswith(self.path):
                utils.delete_folder(project.path)
