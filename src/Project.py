import os
import utils
import sqlite3
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
    def __init__(self, library_path:Optional[str] = None, library_db:Optional[str] = None):
        self.library_path = library_path
        self.library_db = library_db if library_db is not None else ":memory:"
        fexists = os.path.isfile(self.library_db)
        self.db = sqlite3.connect(self.library_db)
        if not fexists:
            self.create_db_if_not_exists()

    def create_db_if_not_exists(self):
        self.db.execute("""CREATE TABLE projects (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME TEXT UNIQUE,
                    PATH TEXT UNIQUE
        );""")

        if self.library_path is not None:
            if os.path.exists(self.library_path):
                params = []
                for item in os.scandir(self.library_path):
                    if item.is_dir():
                        proj = Project(item.path)
                        params.append((proj.name, proj.path))
                if params != []:
                    self.db.executemany("INSERT INTO projects ('NAME', 'PATH') VALUES (?, ?);", params)
        self.db.commit()

    def list_projects(self) -> list[Project]:
        cur = self.db.execute("SELECT PATH FROM projects;")
        return list(map(lambda row: Project(row[0]), cur))

    def get_project(self, name:str):
        cur = self.db.execute("SELECT PATH FROM projects WHERE NAME=?", (name,))

        fo = cur.fetchone()
        if fo:
            return Project(fo[0])

    def add_project(self, project:Project):
        if self.library_path is not None:
            dest = os.path.join(self.library_path, os.path.basename(project.path))
            utils.copy_tree(project.path, dest, exceptions=[project.library_directory, project.relocation_config])
            project = Project(dest)
        self.add_project_link(project)

    def add_project_link(self, project:Project):
        self.db.execute("INSERT INTO projects (NAME, PATH) VALUES (?, ?);", (project.name, project.path))
        self.db.commit()

    def remove_project(self, name:str):
        project = self.get_project(name)
        if project is not None:
            self.db.execute("DELETE FROM projects WHERE NAME=?", (project.name,))
            self.db.commit()

            if self.library_path is not None and project.path.startswith(self.library_path):
                utils.delete_folder(project.path)