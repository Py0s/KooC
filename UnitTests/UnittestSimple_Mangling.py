#!/usr/bin/env python3

import unittest
from __init__ import Mangle, S as S

class Unittest_Mangler(unittest.TestCase):
    """
        Doc: https://docs.python.org/3/library/unittest.html
    """

    def test_VarMangling(self):
        res = Mangle.var('varName', typ = 'char')
        self.assertEqual(res, 'c7varName')
        res = Mangle.var('varName', typ = 'signed char')
        self.assertEqual(res, 'Sc7varName')
        res = Mangle.var('varName', typ = 'int')
        self.assertEqual(res, 'i7varName')
        res = Mangle.var('varName', typ = 'int', sign = S['UNSIGNED'])
        self.assertEqual(res, 'Ui7varName')
        
        self.assertRaises(IndexError, Mangle.var, 'tuturu', typ = 'unknown')

    # def test_funciton_mangling(self):
    #     params = ["int", "long"]
    #     res = Mangle.function("funcName", params = params)
    #     self.assertEquals(res, "__funcName_il")

    #     res = Mangle.function("funcName", namespace = "className", params = params)
    #     self.assertEquals(res, "__funcName_classNameil")

    #     res = Mangle.function("funcName", qual = "const", params = params)
    #     self.assertEquals(res, "funcName_constil")

    #     res = Mangle.function("funcName", qual = "const", namespace = "className", params = params)
    #     self.assertEquals(res, "funcName_il")

if __name__ == "__main__":
    unittest.main()