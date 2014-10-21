#!/usr/bin/env python3
import unittest

#Add your test here
tests = [
    'unittests.test_simple_mangling',
    'unittests.test_kooc_file',
    'unittests.test_import',
]

def main():
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()