import unittest
import json
import os, sys, tempfile

if 'src' not in sys.path:
    sys.path.append("src")
if '../src' not in sys.path:
    sys.path.append("../src")

import utils
import PHPFunctions
class Test_Utils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_json_operations(self):
        json_data = {
            "project_name": "TestProject",
            "project_version": "1.6.5"
        }
        f = tempfile.NamedTemporaryFile('w', delete=False)
        fname = f.name
        f.close()

        utils.write_json(fname, json_data)
        data = utils.read_json(fname)
        os.unlink(fname)
        self.assertEqual(json_data, data, "json operation function alter the data.")
    
    def test_copy_functions(self):
        dir = tempfile.mkdtemp('copyfunctions', 'utils')
        test1_txt = os.path.join(dir, 'test1.txt')
        original_file_contents = "Hello World"
        with open(test1_txt, 'w') as w:
            w.write(original_file_contents)
        
        ndir = os.path.join(dir, 'ndir')
        os.mkdir(ndir)
        test2_txt = os.path.join(dir, 'ndir', 'test2.txt')
        with open(test2_txt, 'w') as w:
            w.write("Second Hello World")

        # Start test
        copied_test1_txt = os.path.join(dir, 'ndir', 'test1.txt')
        utils.copy_file(test1_txt, copied_test1_txt)
        copied_file_exists = os.path.exists(copied_test1_txt)
        copied_file_contents = ''
        if(copied_file_exists):
            with open(copied_test1_txt) as r:
                copied_file_contents = r.read()
        
        dir2 = dir+'2'
        ndir2 = os.path.join(dir2, 'ndir')
        utils.copy_tree(dir, dir2, ['ndir/test1.txt'])
        dir2_test1_txt = os.path.join(dir2, 'test1.txt')
        tree_copied_test1 = os.path.exists(dir2_test1_txt)
        dir2_copied_test1_txt = os.path.join(ndir2, 'test1.txt')
        tree_copied_second_test1 = os.path.exists(dir2_copied_test1_txt)
        dir2_test2_txt = os.path.join(ndir2, 'test2.txt')
        tree_copied_test2 = os.path.exists(dir2_test2_txt)

        utils.delete_folder(dir)
        utils.delete_folder(dir2)

        self.assertTrue(copied_file_exists, "copy_file function didn't copy file")
        self.assertEqual(copied_file_contents, original_file_contents, "copy_file function didn't copy file contents correctly")
        self.assertTrue(tree_copied_test1, "copy_tree didn't copy test1.txt")
        self.assertFalse(tree_copied_second_test1, "copy_tree copied ndir/test1.txt which is in the exceptions")
        self.assertTrue(tree_copied_test2, "copy_tree didn't copy ndir/test2.txt")
    
    def test_delete_folder(self):
        dir = tempfile.mkdtemp('deletefolder', 'utils')
        with open(os.path.join(dir, 'test.txt'), 'w') as w:
            w.write('hi')
        
        dir2 = os.path.join(dir, 'dir2')
        dir3 = os.path.join(dir, 'dir3')
        os.mkdir(dir2)
        os.mkdir(dir3)

        with open(os.path.join(dir3, 'test.txt'), 'w') as w:
            w.write('hi')
        
        utils.delete_folder(dir)
        self.assertFalse(os.path.exists(dir), "delete_folder didn't delete the directory")
    
    def test_php_code_generation(self):
        f = tempfile.NamedTemporaryFile('w', delete=False)
        fname = f.name
        f.close()

        utils.generate_php_config(
            fname,
            {'DEFINE': "YES"},
            False,
            ["test.php"],
            []
        )

        contents = '\n'.join([
            "<?php",
            "require_once('test.php');",
            "define('DEFINE', 'YES');"
        ]) + '\n'

        with open(fname, 'r') as r:
            test1 = (r.read() == contents)
        
        utils.generate_php_config(
            fname,
            {'DEFINE': "YES"},
            True,
            ["test.php"],
            []
        )

        contents = '\n'.join([
            "<?php",
            "require_once('test.php');",
            "$sdir = str_replace('\\\\', '/', __DIR__).'/';",
            "define('DEFINE', $sdir.'YES');",
            "unset($sdir);"
        ]) + '\n'

        with open(fname, 'r') as r:
            test2 = (r.read() == contents)
        
        utils.generate_php_config(
            fname,
            {},
            False,
            [],
            ["load_file"]
        )

        contents = '<?php\n' + PHPFunctions.load_file + '\n'

        with open(fname, 'r') as r:
            test3 = (r.read() == contents)
        os.unlink(fname)
        
        self.assertTrue(test1, "generate_php_config didn't generate correct code for test1")
        self.assertTrue(test2, "generate_php_config doesn't correctly add $sdir (test2)")
        self.assertTrue(test3, "generate_php_config doesn't insert php functions correctly (test3)")
    
    def test_js_code_generation(self):
        f = tempfile.NamedTemporaryFile('w', delete=False)
        fname = f.name
        f.close()

        data = {'TEST': "SUCCESS"}

        utils.generate_js_config(
            fname,
            data
        )

        jsconfig = 'window.relocation = ' + json.dumps(data)

        with open(fname, 'r') as r:
            contents = r.read()
        
        self.assertEqual(jsconfig, contents, "generate_js_config didn't generate correct code")
    
    def test_rooterize_path(self):
        path = 'test/path'
        npath = utils.rooterize_path(path)

        self.assertEqual(npath, '/'+path, "rooterize_path didn't rooterize path correctly")
    
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

if __name__ == "__main__":
    unittest.main()