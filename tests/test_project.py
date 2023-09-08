import unittest
import json
import os, sys, tempfile

if 'src' not in sys.path:
    sys.path.append("src")
if '../src' not in sys.path:
    sys.path.append("../src")

import Project
class Test_ProjectJson(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.data = {
            "project_name": "Project123",
            "project_version": "1.0.1",
            "project_url": "https://github.com/",
            "project_requirements": {"testPack": "https://github.com/testPack"},
            "project_library_directory": "pm_library1",
            "project_input_resource_directory": "resources1",
            "project_output_resource_directory": "pm_resources1",
            "project_relocation_config": "relocation.php1",
            "project_javascript_relocation_config": "relocation.js1"
        }

        f = tempfile.NamedTemporaryFile("w", delete=False)
        json.dump(self.data, f)
        f.close()
        self.pjn = f.name

        super().__init__(*args, **kwargs)

    def test_constructor(self):
        pj = Project.ProjectJson(None)

        self.assertEqual(pj.name, "Project")
        self.assertEqual(pj.version, "1.0.0")
        self.assertEqual(pj.url, "")
        self.assertEqual(pj.requirements, {})
        self.assertEqual(pj.library_directory, "pm_library")
        self.assertEqual(pj.input_resource_directory, "resources")
        self.assertEqual(pj.output_resource_directory, "pm_resources")
        self.assertEqual(pj.relocation_config, 'relocation.php')
        self.assertEqual(pj.javascript_relocation_config, "relocation.js")

        pj2 = Project.ProjectJson(self.pjn)
        for k, v in self.data.items():
            self.assertEqual(pj2.__dict__[k[len("project_"):]], v)

        nepj = Project.ProjectJson("NonExistentProjectFolder/project.json")
        self.assertEqual(nepj.name, "NonExistentProjectFolder")
    
    def test_save(self):
        f = tempfile.NamedTemporaryFile("w", delete=False)
        f.close()

        pj = Project.ProjectJson(self.pjn)
        pj.save(f.name)
        pj2 = Project.ProjectJson(f.name)

        for k in self.data.keys():
            k = k[len("project_"):]
            self.assertEqual(pj.__dict__[k], pj2.__dict__[k])

class Test_Project(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.dir1 = tempfile.mkdtemp("1", "Project")
        self.dir2 = tempfile.mkdtemp("2", "Project")

        self.config1 = {
            "project_name": "TestProject1",
            "project_version": "1.6.5",
            "project_url": "https://github.com/",
            "project_requirements": {},
            "project_library_directory": "pm_library",
            "project_relocation_config": "relocation.php"
        }

        self.config2 = self.config1.copy()
        self.config2["project_name"] = "TestProject2"
        self.config2["project_url"] += "2"

        with open(os.path.join(self.dir1, "project.json"), 'w') as js:
            json.dump(self.config1, js)
        
        with open(os.path.join(self.dir2, "project.json"), 'w') as js:
            json.dump(self.config2, js)

        super().__init__(*args, **kwargs)


    def test_import_project(self):
        p1 = Project.Project(self.dir1)
        p2 = Project.Project(self.dir2)

        p2.import_project(p1)

        dir3 = os.path.join(p2.path, p2.library_directory, os.path.basename(p1.path))
        self.assertTrue(os.path.isdir(dir3), "Project was not imported at all")
        self.assertTrue(os.path.isfile(os.path.join(dir3, p1.relocation_config)), "Project relocation file was not created.")
        self.assertFalse(os.path.isdir(os.path.join(dir3, p1.library_directory)), "Project was relocated with it's library.")
        self.assertTrue(os.path.isdir(os.path.join(p2.path, p2.output_resource_directory, os.path.basename(p1.path))), "Project was imported without it's resources folder.")

        open(os.path.join(p2.path, p2.relocation_config), 'w').close()

        with open(os.path.join(dir3, p1.relocation_config), 'r') as f:
            path = f.read().rstrip().split("require_once('")[-1][:-3]
        self.assertTrue(os.path.isfile(os.path.join(dir3, path)))

    def test_clear_library_folder(self):
        proj = Project.Project(self.dir1)
        lib_path = os.path.join(self.dir1, proj.library_directory)
        proj.clear_library_folder()
        self.assertTrue(os.path.exists(lib_path), "Project library was removed")
    
    def test_clear_resource_folder(self):
        proj = Project.Project(self.dir1)
        res_path = os.path.join(self.dir1, proj.output_resource_directory)
        proj.clear_resource_folder()
        self.assertTrue(os.path.exists(res_path), "Project resource folder was removed")
    
    def test_register_project(self):
        p1 = Project.Project(self.dir1)
        p2 = Project.Project(self.dir2)

        p1.register_project(p2)
        self.assertEqual(p1.requirements, {p2.name: p2.url}, "Project was not registered as a requirement in the second project")
    
    def test_deregister_project(self):
        p1 = Project.Project(self.dir1)
        p2 = Project.Project(self.dir2)

        p1.register_project(p2)
        p1.deregister_project(p2.name)
        self.assertEqual(p1.requirements, {}, "Project was not deregistered from being a requirement in the seconds project")
    
    def test_add_root_relocation(self):
        p1 = Project.Project(self.dir1)
        p1.add_root_relocation()
        self.assertTrue(os.path.isfile(os.path.join(p1.path, p1.relocation_config)), "Project relocation file was not created.")
        self.assertTrue(os.path.isfile(os.path.join(p1.path, p1.javascript_relocation_config)), "Project javascript relocation file was not created.")

class Test_ProjectLibrary(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.tmpdir = tempfile.mkdtemp("lib", "projects")
        self.project1 = os.path.join(self.tmpdir, "Project1")
        self.project2 = os.path.join(self.tmpdir, "Project2")


        os.mkdir(self.project1)
        with open(os.path.join(self.project1, "project.json"), 'w') as js:
            json.dump({"project_name": "Project1", "project_url": "Project1URL"}, js)
        os.mkdir(self.project2)
        with open(os.path.join(self.project2, "project.json"), 'w') as js:
            json.dump({"project_name": "Project2", "project_url": "Project2URL"}, js)
        super().__init__(*args, **kwargs)

    def test_constructor(self):
        pl = Project.ProjectLibrary(self.tmpdir, os.path.join(self.tmpdir, "database.db"))
        projects = [
            Project.Project(self.project1),
            Project.Project(self.project2)
        ]

        templib = os.path.join(self.tmpdir, "TempLib")
        pl2 = Project.ProjectLibrary(templib)
        self.assertTrue(os.path.exists(os.path.join(self.tmpdir, "database.db")), "Temporary database file was not created.")
    
    def test_list_projects(self):
        list_project = tempfile.mkdtemp("list", "project")
        pl = Project.ProjectLibrary(self.tmpdir, os.path.join(self.tmpdir, "database.db"))
        lp = Project.Project(list_project)
        pl.add_project(lp)

        lst = pl.list_projects()
        self.assertEqual(lst[-1].name, lp.name, "list_projects doesn't correctly list all projects in the library.")

    def test_get_project(self):
        pl = Project.ProjectLibrary(self.tmpdir)
        self.assertNotEqual(pl.get_project("Project1"), None)
        self.assertEqual(pl.get_project("NonExistent-Project"), None)
    
    def test_add_project(self):
        # add_project_link is used in add_project, so it's tested as well
        proj3 = tempfile.mkdtemp("3", "Project")
        with open(os.path.join(proj3, "project.json"), 'w') as js:
            json.dump({"project_name": "Project3", "project_url": "Project3URL"}, js)
        proj4 = tempfile.mkdtemp("4", "Project")
        with open(os.path.join(proj4, "project.json"), 'w') as js:
            json.dump({"project_name": "Project4", "project_url": "Project4URL"}, js)

        pl = Project.ProjectLibrary(self.tmpdir)
        pl.add_project(Project.Project(proj4))
        self.assertNotEqual(pl.get_project("Project4"), None)
        pl.add_project(Project.Project(proj3))
        self.assertNotEqual(pl.get_project("Project3"), None)
    
    def test_remove_project(self):
        dir = os.path.join(self.tmpdir, "RemoveProject-Project")
        os.mkdir(dir)
        with open(os.path.join(dir, 'project.json'), 'w') as js:
            json.dump({"project_name": "RemoveProject", "project_url": "RemoveProjectURL"}, js)
        dir2 = tempfile.mkdtemp("Project2", "RemoveProject")
        with open(os.path.join(dir2, 'project.json'), 'w') as js:
            json.dump({"project_name": "RemoveProject2", "project_url": "RemoveProject2URL"}, js)

        pl = Project.ProjectLibrary(self.tmpdir)
        pl.remove_project("RemoveProject")
        pl.remove_project("RemoveProject2")
        self.assertEqual(pl.get_project("RemoveProject"), None)
        self.assertEqual(pl.get_project("RemoveProject2"), None)
        self.assertFalse(os.path.exists(dir), "Project folder was not deleted inside of the library")
        self.assertTrue(os.path.exists(dir2), "Project folder was deleted outside of the library")

if __name__ == "__main__":
    unittest.main()