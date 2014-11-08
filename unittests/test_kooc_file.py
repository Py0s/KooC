#!/usr/bin/env python3

import unittest
import KoocFile

class UnittestKoocFile(unittest.TestCase):

    def setUp(self):
        KoocFile.includePath = "./test"

    # def test_kooc_a_file_empty(self):
    #     self.assertRaises(RuntimeError, KoocFile.kooc_a_file, "empty.kc")
    # def test_kooc_a_file_inexistant(self):
    #     self.assertRaises(RuntimeError, KoocFile.kooc_a_file, "fzifjosdjodgsdffgd.kc")
    # def test_kooc_a_file_bad_extension(self):
    #     self.assertRaises(RuntimeError, KoocFile.kooc_a_file, "muf.c")

    # def test_register_file(self):
    #     KoocFile.register_file("muf.kc")
    #     self.assertTrue(KoocFile.is_file_imported("muf.kc"))
    #     self.assertFalse(KoocFile.is_file_imported("muf.kh"))
    #     self.assertFalse(KoocFile.is_file_imported("test.kc"))

if __name__ == "__main__":
    unittest.main()