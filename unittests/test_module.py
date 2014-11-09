#!/usr/bin/env python3

import unittest
from KoocGrammar import KoocG
from cnorm.parsing.declaration import Declaration
from KoocGrammar import Module
from cnorm.passes import to_c
import KoocFile

class UnittestModule(unittest.TestCase):

    def setUp(self):
        self.cparse = Declaration()
        self.kparse = KoocG()

    def tearDown(self):
        self.cparse = None
        self.kparse = None
        KoocFile.debugCleanAll()
        if hasattr(self, "res") and not hasattr(self.res, "to_c"):
            self.assertFalse(self.res.diagnostic.get_content())

    ## SIMPLE TO MORE COMPLEX TEST OF VALIDS MODULES
    def test_empty_module(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "")
    def test_declaration_variable(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             void test;
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern void M4Test__v4test;\n")
    def test_declaration_assignement_variable(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             int test = 42;
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern int M4Test__i4test;\n")
    def test_declaration_function_implicit_void(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             void test();
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern void M4Test__v4testv();\n")
    def test_declaration_function_explicit_void(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             void test(void);
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern void M4Test__v4testv(void);\n")
    def test_declaration_function(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             char *test(int **toto, float tata[]);
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                        "extern char *M4Test__Pc4testPPiAf(int **toto, float tata[]);\n")
    def test_variable_overload(self):
        self.res = self.kparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                float tuturu;
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern int M6Mayuri__i6tuturu;\nextern float M6Mayuri__f6tuturu;\n")
    def test_variable_and_function_with_no_param(self):
        self.res = self.kparse.parse(
            """
            @module Mayuri
            {
                int tuturu;
                int tuturu();
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern int M6Mayuri__i6tuturu;\nextern int M6Mayuri__i6tuturuv();\n")
    def test_function_return_value_overload(self):
        self.res = self.kparse.parse(
            """
            @module Mayuri
            {
                int tuturu(float toto);
                float tuturu(float tutu);
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern int M6Mayuri__i6tuturuf(float toto);\n\
extern float M6Mayuri__f6tuturuf(float tutu);\n")
    def test_function_params_value_overload(self):
        self.res = self.kparse.parse(
            """
            @module Mayuri
            {
                double **tuturu(char toto[], void* ptr[]);
                double** tuturu(int tutu);
            }
            """)
        self.assertEqual(str(self.res.to_c()),
                         "extern double **M6Mayuri__PPd6tuturuAcAPv(char toto[], void *ptr[]);\n\
extern double **M6Mayuri__PPd6tuturui(int tutu);\n")


    def test_const_ptr_variable(self):
        waited = self.cparse.parse("""
extern const int *M4Test__Pi4test;
            """)
        self.res = self.kparse.parse(
            """
            @module Test
            {
             int const* test;
            }
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_complex_variable(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             auto unsigned int const* const* test;
            }
            """)
        waited = self.cparse.parse("""
extern auto unsigned int const* const* M4Test__PPui4test;
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))


# JAI FAIT DE LA MERDE
#     def test_module_pointer(self):
#         self.res = self.kparse.parse(
#             """
#             @module Titor
#             {
#              void send_dmail(Titor *this, char *mail);
#             }
#             """)
#         waited = self.cparse.parse("""
# extern void MTitor__v4send_dmailS5TitorPc(Titor *this, char *mail);
#             """)
#         if not hasattr(self.res, "to_c"):
#             self.assertFalse("!!! A WILD ERROR APPEARS : ", self.res.diagnostic.get_content())
#         self.assertEqual(str(self.res.to_c())).to_c()), waited.to_c()))

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
    ##     self.res = self.cparse.parse(
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
    ##     self.assertEqual(str(self.res.to_c()),
    ##                     "")
    ## def test_koocCall_in_function(self):
    ##     self.res = self.cparse.parse(
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
    ##     self.assertEqual(str(self.res.to_c()),
    ##                     "")
    ## def test_typage_ret_koocCall_in_function(self):
    ##     self.res = self.cparse.parse(
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
    ##     self.assertEqual(str(self.res.to_c()),
    ##                     "")
    ## def test_typage_var_koocCall_in_function(self):
    ##     self.res = self.cparse.parse(
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
    ##     self.assertEqual(str(self.res.to_c()),
    ##                     "")

if __name__ == "__main__":
    unittest.main()
