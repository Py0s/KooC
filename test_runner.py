#!/usr/bin/env python3
import unittest
from unittests import unittest_simple_mangling as sm

def suite():
    test_suite = unittest.TestSuite()
    #add your test here
    test_suite.addTest(unittest.makeSuite(sm.UnittestSimpleMangling))
    return test_suite

mySuit = suite()
runner = unittest.TextTestRunner()
runner.run(mySuit)