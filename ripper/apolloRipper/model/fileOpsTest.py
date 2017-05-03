import unittest
from model.fileOps import move_file
import os
import stat

class fileOpsTest(unittest.TestCase):

    def test_move_file(self):
        old_filename = "old_test"
        new_filename = "new_test"
        test_chars = "123456"

        f = open("old_test", "wb+")
        f.write(test_chars)
        f.close()

        move_file(old_filename,new_filename)

        self.assertTrue(os.path.exists(new_filename))
        self.assertFalse(os.path.exists(old_filename))
        os.remove(new_filename)