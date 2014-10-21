#!/usr/bin/env python3

import unittest
import mangler.simple_mangling as sm

class UnittestSimpleMangling(unittest.TestCase):
    """
        Doc: https://docs.python.org/3/library/unittest.html
    """

    def test_ident_mangling(self):
        ident = 'MyName'
        self.assertEqual(sm.identifier(ident), str(len(ident)) + ident)

    def test_var_mangling(self):
        res = sm.type('varName', typ = 'char')
        self.assertEqual(res, 'c7varName')
        res = sm.type('varName', typ = 'signed char')
        self.assertEqual(res, 'Sc7varName')
        res = sm.type('varName', typ = 'int')
        self.assertEqual(res, 'i7varName')
        res = sm.type('varName', typ = 'int', sign = sm.S['UNSIGNED'])
        self.assertEqual(res, 'Ui7varName')
        
        self.assertRaises(IndexError, sm.type, 'tuturu', typ = 'unknown')

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