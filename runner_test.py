#!/usr/bin/env python3
import sys
import unittest

#Add your test here
tests = [
    'unittests.test_simple_mangling',
    'unittests.test_kooc_file',
    'unittests.test_import',
    'unittests.test_class',
    'unittests.test_module',
    'unittests.test_kooccall',
]
    # 'unittests.test_newtest',

def main():
    sys.tracebacklimit = 0
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
   ## TEST OF OVERLOADS WITH DIFFERENTS STORAGES, QUALIFIERS OR SPECIFIER
    # Little reminder :
    # Storages = meta.enum('AUTO', 'REGISTER', 'TYPEDEF',
    #                  'STATIC', 'EXTERN', 'INLINE',
    #                  'VIRTUAL', 'EXPLICIT',
    #                  'FORCEINLINE', 'THREAD')
    # Qualifiers = meta.enum('AUTO', 'CONST', 'VOLATILE', 'RESTRICT',
    #                    'W64', 'STDCALL', 'CDECL',
    #                    'PTR32', 'PTR64', 'FASTCALL')
    # Specifiers = meta.enum('AUTO', 'STRUCT', 'UNION', 'ENUM', 'LONG',
    #                    'LONGLONG', 'SHORT')