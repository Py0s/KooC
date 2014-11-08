#!/usr/bin/env python3

import unittest
from KoocGrammar import KoocG
from KoocGrammar import Module
from cnorm.passes import to_c
import KoocFile

class UnittestModule(unittest.TestCase):

    def setUp(self):
        self.cparse = KoocG()

    def tearDown(self):
        self.cparse = None
        KoocFile.debugCleanAll()

    ## SIMPLE TO MORE COMPLEX TEST OF VALIDS MODULES
    def test_empty_module(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
            }
            """).to_c())
        self.assertEqual(res,
                         "")
    def test_declaration_variable(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             void test;
            }
            """).to_c())
        self.assertEqual(res,
                         "extern void M4Test__v4test;\n")
    def test_declaration_assignement_variable(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             int test = 42;
            }
            """).to_c())
        self.assertEqual(res,
                         "extern int M4Test__i4test;\n")
    def test_declaration_function_implicit_void(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             void test();
            }
            """).to_c())
        self.assertEqual(res,
                         "extern void M4Test__v4testv();\n")
    def test_declaration_function_explicit_void(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             void test(void);
            }
            """).to_c())
        self.assertEqual(res,
                         "extern void M4Test__v4testv(void);\n")
    def test_declaration_function(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             char *test(int **toto, float tata[]);
            }
            """).to_c())
        self.assertEqual(res,
                        "extern char *M4Test__Pc4testPPiAf(int **toto, float tata[]);\n")
    def test_variable_overload(self):
        res = str(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                float tuturu;
            }
            """).to_c())
        self.assertEqual(res,
                         "extern int M6Mayuri__i6tuturu;\nextern float M6Mayuri__f6tuturu;\n")
    def test_variable_and_function_with_no_param(self):
        res = str(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                int tuturu();
            }
            """).to_c())
        self.assertEqual(res,
                         "extern int M6Mayuri__i6tuturu;\nextern int M6Mayuri__i6tuturuv();\n")
    def test_function_return_value_overload(self):
        res = str(self.cparse.parse(
            """
            @module Mayuri
            {
                int tuturu(float toto);
                float tuturu(float tutu);
            }
            """).to_c())
        self.assertEqual(res,
                         "extern int M6Mayuri__i6tuturuf(float toto);\n\
extern float M6Mayuri__f6tuturuf(float tutu);\n")
    def test_function_params_value_overload(self):
        res = str(self.cparse.parse(
            """
            @module Mayuri
            {
                double **tuturu(char toto[], void* ptr[]);
                double** tuturu(int tutu);
            }
            """).to_c())
        self.assertEqual(res,
                         "extern double **M6Mayuri__PPd6tuturuAcAPv(char toto[], void *ptr[]);\n\
extern double **M6Mayuri__PPd6tuturui(int tutu);\n")

    ## TODO : TESTS WITH SOME FUNCTION POINTER

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

    # TODO!!

    ## TEST OF INVALIDS MODULES?

    # TODO!!?

    ## TODO : A mettre dans test_implementation
    ## def test_simple_koocCall_in_function(self):
    ##     res = str(self.cparse.parse(
    ##         """
    ##         @module Test1
    ##         {
    ##          int test1();
    ##         }
    ##         @module Test2
    ##         {
    ##           void test2([Test1 test1]);
    ##         }
    ##         """).to_c())
    ##     self.assertEqual(res,
    ##                     "")
    ## def test_koocCall_in_function(self):
    ##     res = str(self.cparse.parse(
    ##         """
    ##         @module Test1
    ##         {
    ##          float toto;
    ##         }
    ##         @module Test2
    ##         {
    ##          int test2(float toto);
    ##         }
    ##         @module Test3
    ##         {
    ##           void test2([Test2 test2 :[Test1.toto]]);
    ##         }
    ##         """).to_c())
    ##     self.assertEqual(res,
    ##                     "")
    ## def test_typage_ret_koocCall_in_function(self):
    ##     res = str(self.cparse.parse(
    ##         """
    ##         @module Test1
    ##         {
    ##          int test1();
    ##         }
    ##         @module Test2
    ##         {
    ##           void test2(@!(int)[Test1 test1]);
    ##         }
    ##         """).to_c())
    ##     self.assertEqual(res,
    ##                     "")
    ## def test_typage_var_koocCall_in_function(self):
    ##     res = str(self.cparse.parse(
    ##         """
    ##         @module Test1
    ##         {
    ##          float toto;
    ##         }
    ##         @module Test2
    ##         {
    ##          int test1(float toto);
    ##         }
    ##         @module Test3
    ##         {
    ##           void test2(@!(int)[Test2 test2 :(float)[Test1.toto]]);
    ##         }
    ##         """).to_c())
    ##     self.assertEqual(res,
    ##                     "")

if __name__ == "__main__":
    unittest.main()
