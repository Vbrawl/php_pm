import unittest
import tempfile
import json
import os, sys

sys.path.append("src")

import utils
class Test_Utils(unittest.TestCase):
    def test_read_json(self):
        data = {
            "project_name": "TestProject",
            "project_version": "1.6.5"
        }


        f = tempfile.TemporaryFile("w", delete=False)
        fname = f.name
        json.dump(data, f)
        f.close()

        data2 = utils.read_json(fname)
        self.assertEqual(data, data2, "Data was altered.")
    
    def test_write_json(self):
        data = {
            "project_name": "TestProject",
            "project_version": "1.6.5"
        }
        f = tempfile.TemporaryFile("w", delete=False)
        fname = f.name
        f.close()
        utils.write_json(fname, data)

        with open(fname, 'r') as file_:
            data2 = json.load(file_)
        
        self.assertEqual(data, data2, "Data was altered.")

    def test_copy_file(self):
        f = tempfile.TemporaryFile("w", delete=False)
        f.close()
        utils.copy_file(f.name, f.name+".2")

        self.assertTrue(os.path.isfile(f.name), "Source file does not exist.")
        self.assertTrue(os.path.isfile(f.name+".2"), "Destination file does not exist.")

    def test_copy_tree(self):
        directory = tempfile.mkdtemp("tree", "copy")
        open(os.path.join(directory, "testFile"), "w").close()

        utils.copy_tree(directory, directory+"2")

        self.assertTrue(os.path.isfile(os.path.join(directory, "testFile")), "Source directory does not exist.")
        self.assertTrue(os.path.isfile(os.path.join(directory+"2", "testFile")), "Destination directory does not exist.")
    

    def test_delete_folder(self):
        directory = tempfile.mkdtemp("delete", "folders")
        os.mkdir(os.path.join(directory, "hello"))
        os.mkdir(os.path.join(directory, "hello2"))
        os.mkdir(os.path.join(directory, "hello", "hi"))
        open(os.path.join(directory, "hello", 'hi.txt'), 'w').close()
        open(os.path.join(directory, "hello", 'hi', "hello.txt"), 'w').close()
        open(os.path.join(directory, "hello2", 'hi.txt'), 'w').close()

        self.assertTrue(os.path.exists(directory), "Project directory was not detected")
        utils.delete_folder(directory)
        self.assertFalse(os.path.exists(directory), "Project directory was not removed")

        self.assertRaises(FileNotFoundError, utils.delete_folder, directory)
    
    def test_generate_php_config(self):
        definitions = {
            "test1": "hi",
            "test2": "hi2"
        }

        output = """<?php
define("test1", "hi");
define("test2", "hi2");"""

        f = tempfile.TemporaryFile("w", delete=False)
        f.close()
        utils.generate_php_config(f.name, definitions)
        with open(f.name, 'r') as inp:
            generated = inp.read()
        self.assertEqual(output, generated, "PHP code generation doesn't generate the expected code.")
    
    def test_binary_search(self):
        testlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Test every possible case
        for i in range(0, 12):
            expected = i if i != 11 else None
            self.assertEqual(utils.binary_search(testlist, i), expected)

        rev_testlist = list(reversed(testlist))
        for i in range(-1, 11):
            num = 10 - i
            expected = i if i != -1 else None
            self.assertEqual(utils.binary_search(rev_testlist, num, ascending=False), expected)

        testlist2 = list(map(lambda x:[x], testlist))
        for i in range(0, 12):
            expected = i if i != 11 else None
            self.assertEqual(utils.binary_search(testlist2, i, key = lambda x: x[0]), expected)





import Project
class Test_Project(unittest.TestCase):
    def test_import_project(self):
        dir1 = tempfile.mkdtemp("1", "project")
        dir2 = tempfile.mkdtemp("2", "project")

        project_json_1 = {
            "project_name": "TestProject1",
            "project_version": "1.6.5",
            "project_url": "https://github.com/",
            "project_requirements": {},
            "project_library_directory": "pm_library"
        }

        project_json = open(os.path.join(dir1, "project.json"), 'w')
        json.dump(project_json_1, project_json)
        project_json.close()

        project_json_2 = project_json_1
        project_json_2["project_name"] = "TestProject2"

        project_json = open(os.path.join(dir2, "project.json"), "w")
        json.dump(project_json_2, project_json)
        project_json.close()

        p1 = Project.Project(dir1)
        p2 = Project.Project(dir2)

        p2.import_project(p1)

        dir3 = os.path.join(p2.path, p2.library_directory, p1.name)
        self.assertTrue(os.path.isdir(dir3), "Project was not imported at all")

    def test_clear_library_folder(self):
        dir3 = tempfile.mkdtemp("3", "project")
        proj3 = Project.Project(dir3)
        lib_path = os.path.join(dir3, proj3.library_directory)
        proj3.clear_library_folder()
        self.assertTrue(os.path.exists(lib_path), "Project library was removed")
    
    def test_register_project(self):
        dir4 = tempfile.mkdtemp("4", "project")
        dir5 = tempfile.mkdtemp("5", "project")
        with open(os.path.join(dir5, "project.json"), 'w') as js:
            json.dump({"project_name": "TestName", "project_url": "TestURL"}, js) 
        p = Project.Project(dir4)
        self.assertEqual(p.requirements, {})
        p.register_project(Project.Project(dir5))
        self.assertEqual(p.requirements, {"TestName": "TestURL"})

class Test_ProjectJson(unittest.TestCase):
    def test_constructor(self):
        pj = Project.ProjectJson(None)

        self.assertEqual(pj.name, "Project")
        self.assertEqual(pj.version, "1.0.0")
        self.assertEqual(pj.url, "")
        self.assertEqual(pj.requirements, {})
        self.assertEqual(pj.library_directory, "pm_library")


        f = tempfile.TemporaryFile("w", delete=False)
        json.dump({
            "project_name": "Project123",
            "project_version": "1.0.1",
            "project_url": "https://github.com/",
            "project_requirements": {"testPack": "https://github.com/testPack"},
            "project_library_directory": "pm_library1",
            "project_relocation_config": "relocation.php1"
        }, f)
        f.close()

        pj2 = Project.ProjectJson(f.name)
        self.assertEqual(pj2.name, "Project123")
        self.assertEqual(pj2.version, "1.0.1")
        self.assertEqual(pj2.url, "https://github.com/")
        self.assertEqual(pj2.requirements, {"testPack": "https://github.com/testPack"})
        self.assertEqual(pj2.library_directory, "pm_library1")
        self.assertEqual(pj2.relocation_config, "relocation.php1")
    
    def save(self):
        pj = Project.ProjectJson(None)
        f = tempfile.TemporaryFile("w", delete=False)
        f.close()

        pj.save(f.name)
        pj2 = Project.ProjectJson(f.name)

        self.assertEqual(pj, pj2, "Data was not correctly saved")


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

    def test_constructor_AND_load_projects(self):
        pl = Project.ProjectLibrary(self.tmpdir)
        projects = [
            Project.Project(self.project1),
            Project.Project(self.project2)
        ]

        found_projects = 0
        for i, proj in enumerate(pl.projects):
            if proj.name == projects[i].name:
                found_projects += 1
        
        self.assertEqual(found_projects, len(projects))
    
    def test_get_project(self):
        pl = Project.ProjectLibrary(self.tmpdir)
        self.assertNotEqual(pl.get_project("Project1"), None)
        self.assertEqual(pl.get_project("Project4"), None)
    
    def test_add_project(self):
        proj3 = tempfile.mkdtemp("3", "Project")
        with open(os.path.join(proj3, "project.json"), 'w') as js:
            json.dump({"project_name": "Project3", "project_url": "Project3URL"}, js)
        pl = Project.ProjectLibrary(self.tmpdir)
        pl.add_project(Project.Project(proj3))

        self.assertNotEqual(pl.get_project("Project3"), None)

if __name__ == "__main__":
    unittest.main()