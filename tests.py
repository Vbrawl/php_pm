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
        self.assertEqual(data, data2)
    
    def test_copy_file(self):
        f = tempfile.TemporaryFile("w", delete=False)
        f.close()
        utils.copy_file(f.name, f.name+".2")

        self.assertTrue(os.path.isfile(f.name))
        self.assertTrue(os.path.isfile(f.name+".2"))

    def test_copy_tree(self):
        directory = tempfile.mkdtemp("tree", "copy")
        open(os.path.join(directory, "testFile"), "w").close()

        utils.copy_tree(directory, directory+"2")

        self.assertTrue(os.path.isfile(os.path.join(directory, "testFile")))
        self.assertTrue(os.path.isfile(os.path.join(directory+"2", "testFile")))



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
        p3 = Project.Project(dir3)

        self.assertEqual(p1.name, p3.name)
        self.assertEqual(p1.version, p3.version)
        self.assertEqual(p1.url, p3.url)
        self.assertEqual(p1.requirements, p3.requirements)
        self.assertEqual(p1.library_directory, p3.library_directory)

if __name__ == "__main__":
    unittest.main()