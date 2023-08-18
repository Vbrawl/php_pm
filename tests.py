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


        f = tempfile.NamedTemporaryFile("w", delete=False)
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
        f = tempfile.NamedTemporaryFile("w", delete=False)
        fname = f.name
        f.close()
        utils.write_json(fname, data)

        with open(fname, 'r') as file_:
            data2 = json.load(file_)
        
        self.assertEqual(data, data2, "Data was altered.")

    def test_copy_file(self):
        f = tempfile.NamedTemporaryFile("w", delete=False)
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

        requirements = ["test_file.php"]

        output = """<?php
require_once('test_file.php');
$sdir = str_replace('\\\\', '/', __DIR__);
define('test1', $sdir.'hi');
define('test2', $sdir.'hi2');
unset($sdir);
"""

        f = tempfile.NamedTemporaryFile("w", delete=False)
        f.close()
        utils.generate_php_config(f.name, definitions, True, requirements)
        with open(f.name, 'r') as inp:
            generated = inp.read()
        self.assertEqual(output, generated, "PHP code generation doesn't generate the expected code.")

        output = """<?php
define('test1', 'hi');
define('test2', 'hi2');
"""
        utils.generate_php_config(f.name, definitions, False)
        with open(f.name, 'r') as inp:
            generated = inp.read()
        self.assertEqual(output, generated, "PHP code generation doesn't generate the expected code.")
    
    def test_binary_search(self):
        emptylist = []
        self.assertEqual(utils.binary_search(emptylist, 11), None)

        singleitemlist = [1]
        self.assertEqual(utils.binary_search(singleitemlist, 1), 0)
        self.assertEqual(utils.binary_search(singleitemlist, 11), None)

        testlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i in range(0, 12):
            expected = i if i != 11 else None
            self.assertEqual(utils.binary_search(testlist, i), expected)

        rev_testlist = list(reversed(testlist))
        for i in range(-1, 11):
            num = 10 - i
            expected = i if i != -1 else None
            self.assertEqual(utils.binary_search(rev_testlist, num), expected)

        testlist2 = list(map(lambda x:[x], testlist))
        for i in range(0, 12):
            expected = i if i != 11 else None
            self.assertEqual(utils.binary_search(testlist2, i, key = lambda x: x[0]), expected)
    
    def test_append_sorted(self):
        lst = []
        utils.append_sorted(lst, 1)
        utils.append_sorted(lst, 10)
        self.assertEqual(lst, [1, 10])

        utils.append_sorted(lst, 5)
        self.assertEqual(lst, [1, 5, 10])

        lst.reverse() # [10, 5, 1]

        utils.append_sorted(lst, 3)
        self.assertEqual(lst, [10, 5, 3, 1])

        utils.append_sorted(lst, 2, ascending=False)
        self.assertEqual(lst, [10, 5, 3, 2, 1])

        utils.append_sorted(lst, 2)
        self.assertEqual(lst, [10, 5, 3, 2, 2, 1])

        utils.append_sorted(lst, 0)
        self.assertEqual(lst, [10, 5, 3, 2, 2, 1, 0])

        utils.append_sorted(lst, 11)
        self.assertEqual(lst, [11, 10, 5, 3, 2, 2, 1, 0])

        utils.append_sorted(lst, 11)
        self.assertEqual(lst, [11, 11, 10, 5, 3, 2, 2, 1, 0])
    
    def test_remove_common_path(self):
        a = "/a/b/c/d/e/f/g"
        subp = "/a/b/c/d/e/awd/awpdok"

        res = utils.remove_common_path(a, subp)
        res2 = utils.remove_common_path(a, subp, join=False)
        expected_res = (["f", "g"], ["awd", "awpdok"])

        self.assertEqual(res, tuple(map(lambda x: '/'.join(x), expected_res)))
        self.assertEqual(res2, expected_res)
    
    def test_parts_in_path(self):
        a = '/a/b/c/d/e/f/g'
        EAres = ["a", "b", "c", "d", "e", "f", "g"]
        Ares = utils.parts_in_path(a)
        self.assertEqual(Ares, EAres)

        b = "/a/b/c/d/e/f/g//"
        EBres = ["a", "b", "c", "d", "e", "f", "g"]
        Bres = utils.parts_in_path(b)
        self.assertEqual(Bres, EBres)





import Project
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

    def test_clear_library_folder(self):
        proj = Project.Project(self.dir1)
        lib_path = os.path.join(self.dir1, proj.library_directory)
        proj.clear_library_folder()
        self.assertTrue(os.path.exists(lib_path), "Project library was removed")
    
    def test_register_project(self):
        p1 = Project.Project(self.dir1)
        p2 = Project.Project(self.dir2)
        self.assertEqual(p1.requirements, {})
        p1.register_project(p2)
        self.assertEqual(p1.requirements, {p2.name: p2.url})
    
    def test_add_root_relocation(self):
        p1 = Project.Project(self.dir1)
        p1.add_root_relocation()
        self.assertTrue(os.path.isfile(os.path.join(p1.path, p1.relocation_config)), "Project relocation file was not created.")

class Test_ProjectJson(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.data = {
            "project_name": "Project123",
            "project_version": "1.0.1",
            "project_url": "https://github.com/",
            "project_requirements": {"testPack": "https://github.com/testPack"},
            "project_library_directory": "pm_library1",
            "project_relocation_config": "relocation.php1"
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

        pj2 = Project.ProjectJson(self.pjn)
        for k, v in self.data.items():
            self.assertEqual(pj2.__dict__[k[len("project_"):]], v)

        nepj = Project.ProjectJson("NonExistentProjectFolder/project.json")
        self.assertEqual(nepj.name, "NonExistentProjectFolder")
    
    def save(self):
        f = tempfile.NamedTemporaryFile("w", delete=False)
        f.close()

        pj = Project.ProjectJson(self.pjn)
        pj.save(f.name)
        pj2 = Project.ProjectJson(f.name)

        for k in self.data.keys():
            k = k[len("project_"):]
            self.assertEqual(pj.__dict__[k], pj2.__dict__[k])


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

        templib = os.path.join(self.tmpdir, "TempLib")
        pl2 = Project.ProjectLibrary(templib)
        self.assertTrue(os.path.exists(templib), "Temporary inexistent folder was not created.")
    
    def test_get_project(self):
        pl = Project.ProjectLibrary(self.tmpdir)
        self.assertNotEqual(pl.get_project("Project1"), None)
        self.assertEqual(pl.get_project("NonExistent-Project"), None)
    
    def test_add_project(self):
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
        self.assertEqual(pl.projects[2].name, "Project3", "Project List lost sorting")
    
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
