import os
import utils




class Project:
    def __init__(self, path:str, project_json_filename:str = "project.json"):
        project_json = utils.read_json(os.path.join(path, project_json_filename))

        self.path = path
        self.name = project_json["project_name"]
        self.version = project_json["project_version"]
        self.url = project_json["project_url"]
        self.requirements = project_json["project_requirements"]
        self.library_directory = project_json["project_library_directory"]
        if not self.library_directory: self.library_directory = "pm_library"
    
    def import_project(self, project: 'Project'):
        src = project.path
        dest = os.path.join(self.path, self.library_directory, project.name)

        utils.copy_tree(src, dest)