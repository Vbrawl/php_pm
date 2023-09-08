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

if __name__ == "__main__":
    unittest.main()