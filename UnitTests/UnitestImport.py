#!/usr/bin/env python3

import unittest
from __init__ import Import

class Unittest_Import(unittest.TestCase):
    """
        Doc: https://docs.python.org/3/library/unittest.html
    """

    def test_funciton_mangling(self):
        res = Import.function("functionName", params = "int", params = "long")
        res = Import.function("functionName", namespace = "className", params = "int", params = "long")
        res = Import.function("functionName", qual = "const", params = "int", params = "long")
        res = Import.function("functionName", qual = "const", namespace = "className", params = "int", params = "long")

if __name__ == "__main__":
    unittest.main()
