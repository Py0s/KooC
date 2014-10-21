#!/usr/bin/env python3
import sys
import unittest

#Add your test here
tests = [
    'unittests.test_simple_mangling'
]

def main():
    suite = unittest.TestSuite()
    if len(sys.argv) > 1:
        for test in sys.argv[1:]:
            test = test.replace('.py', '')
            test = test.replace('/', '.')
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))
    else:
        for test in tests:
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))
    unittest.TextTestRunner().run(suite)

if __name__ == '__main__':
    main()