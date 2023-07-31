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



if __name__ == "__main__":
    unittest.main()