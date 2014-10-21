#!/usr/bin/env python3
import unittest

#Add your test here
tests = [
    'unittests.test_simple_mangling'
]

def main():
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()