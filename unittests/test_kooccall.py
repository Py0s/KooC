#!/usr/bin/env python3

import unittest
from cnorm.parsing.declaration import Declaration
from KoocGrammar import KoocG
from KoocGrammar import Module
from cnorm.passes import to_c
import KoocFile

class UnittestKooccall(unittest.TestCase):

    def setUp(self):
        self.cparse = Declaration()
        self.kparse = KoocG()

    def tearDown(self):
        self.cparse = None
        self.kparse = None
        KoocFile.debugCleanAll()
        if hasattr(self, "res") and not hasattr(self.res, "to_c"):
            self.assertFalse(self.res.diagnostic.get_content())


    def test_simple_function_call(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             int test(void);
            }
            int main()
            {
              [Test test];
            }
            """)
        waited = self.cparse.parse("""
extern int M4Test__i4testv(void);
int main()
{
    M4Test__i4testv();
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_simple_variable_call(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             int test;
            }
            int main()
            {
              [Test.test];
            }
            """)
        waited = self.cparse.parse("""
extern int M4Test__i4test;
int main()
{
    M4Test__i4test;
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_complex_variable_call(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             auto unsigned int const* const* test;
            }
            int main()
            {
              [Test.test];
            }
            """)
        #TODO : c'est quoi le mangling de cette merde ?
        waited = self.cparse.parse("""
extern const unsigned int *const *M4Test__Pi4test;
int main()
{
    M4Test__Pi4test;
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))


    # def test_simple_variable_call(self):
    #     self.res = self.kparse.parse(
    #         """
    #         int main()
    #         {
    #           [Test.test];
    #         }
    #         """)
    #     print(res.diagnostic.get_content())
    #     waited = self.cparse.parse("""
    # M4Test__i4test;
    #         """).to_c())
    #     print("RESULT = ", res, "\n")
    #     print("WAITED = ", waited, "\n")
    #     self.assertEqual(res, waited)


    def test_simple_variable_assign_call(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             int test;
            }
            int main()
            {
              int a = [Test.test];
            }
            """)
        waited = self.cparse.parse("""
extern int M4Test__i4test;
int main()
{
    int a = M4Test__i4test;
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_one_arg_call(self):
        self.res = self.kparse.parse(
            """
            @module Test
            {
             int test(int toto);
            }
            int main()
            {
              [Test test :(int)42];
            }
            """)
        waited = self.cparse.parse("""
extern int M4Test__i4testi(int toto);
int main()
{
    M4Test__i4testi(42);
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_two_arg_call(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             void send_dmail(void *this, char *mail);
            }
            int main()
            {
                char *mail = "Watashi wa mad scientist !";
              @!(void)[Titor send_dmail :(void *)0 :(char *)mail];
            }
            """)
        waited = self.cparse.parse("""
extern void M5Titor__v10send_dmailPvPc(void *this, char *mail);
int main()
{
    char *mail = "Watashi wa mad scientist !";
    M5Titor__v10send_dmailPvPc(0, mail);
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_return_type_inferred_call(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             void send_dmail(void *this, char *mail);
             void send_dmail(char *mail);
            }
            int main()
            {
                char *mail = "Watashi wa mad scientist !";
              [Titor send_dmail :(void *)0 :(char *)mail];
            }
            """)
        waited = self.cparse.parse("""
extern void MTitor__v10send_dmailPvPc(void *this, char *mail);
extern void MTitor__v10send_dmailPc(char *mail);
int main()
{
    char *mail = "Watashi wa mad scientist !";
    MTitor__v10send_dmailPvPc(0, mail);
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_empty_params_types_inferred_call(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(void);
            }
            int main()
            {
              printf("%s\n", @!(char *)[Titor get_dmail]);
            }
            """)
        waited = self.cparse.parse("""
extern char* MTitor__Pc9get_dmailv(void);
int main()
{
    printf("%s\n", MTitor__Pc9get_dmailv(void));
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_int_params_types_inferred_call(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(int index);
             void *get_dmail(int index);
            }
            int main()
            {
              printf("%s\n", @!(char *)[Titor get_dmail :42]);
            }
            """)
        waited = self.cparse.parse("""
extern char* MTitor__Pc9get_dmaili(int index);
extern void* MTitor__Pv9get_dmaili(int index);
int main()
{
    printf("%s\n", MTitor__Pc9get_dmaili(42));
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_all_inferred_call(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(int index);
            }
            int main()
            {
              printf("%s\n", [Titor get_dmail :42]);
            }
            """)
        waited = self.cparse.parse("""
extern char* MTitor__Pc9get_dmaili(int index);
int main()
{
    printf("%s\n", MTitor__Pc9get_dmaili(42));
}
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_overload_charptr_call(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(int index);
             float get_dmail(int index);
            }
            int main()
            {
              printf("%s\n", @!(char *)[Titor get_dmail :(int)42]);
            }
            """)
        waited = self.cparse.parse(
            """
            extern char* M5Titor__Pc9get_dmaili(int index);
            extern float M5Titor__f9get_dmaili(int index);
            int main()
            {
            printf("%s\n", M5Titor__Pc9get_dmaili(42));
            }
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_overload_floatcall(self):
        self.res = self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(int index);
             float get_dmail(int index);
            }
            int main()
            {
              printf("%s\n", @!(float)[Titor get_dmail :(int)42]);
            }
            """)
        waited = self.cparse.parse(
            """
            extern char* M5Titor__Pc9get_dmaili(int index);
            extern float M5Titor__f9get_dmaili(int index);
            int main()
            {
            printf("%s\n", M5Titor__f9get_dmaili(42));
            }
            """)
        self.assertEqual(str(self.res.to_c()), str(waited.to_c()))

    def test_function_impossible_inferred_return_type(self):
        with self.assertRaises(RuntimeError) as cm:
            print(self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(int index);
             float get_dmail(int index);
            }
            int main()
            {
              printf("%s\n", [Titor get_dmail :(int)42]);
            }
            """))

    def test_function_impossible_inferred_params_type(self):
        with self.assertRaises(RuntimeError) as cm:
            print(self.kparse.parse(
            """
            @module Titor
            {
             char *get_dmail(int index);
             char *get_dmail(float date);
            }
            int main()
            {
              printf("%s\n", [Titor get_dmail :42]);
            }
            """))








    # def test_koocCall_in_function(self):
    #     self.res = str(self.cparse.parse(
    #         """
    #         @module Test1
    #         {
    #          float toto;
    #         }
    #         @module Test2
    #         {
    #          int test2(float toto);
    #         }
    #         @module Test3
    #         {
    #           void test2([Test2 test2 :[Test1.toto]]);
    #         }
    #         """).to_c())
    #     self.assertEqual(res,
    #                     "")
    # def test_typage_ret_koocCall_in_function(self):
    #     self.res = str(self.cparse.parse(
    #         """
    #         @module Test1
    #         {
    #          int test1();
    #         }
    #         @module Test2
    #         {
    #           void test2(@!(int)[Test1 test1]);
    #         }
    #         """).to_c())
    #     self.assertEqual(res,
    #                     "")
    # def test_typage_var_koocCall_in_function(self):
    #     self.res = str(self.cparse.parse(
    #         """
    #         @module Test1
    #         {
    #          float toto;
    #         }
    #         @module Test2
    #         {
    #          int test1(float toto);
    #         }
    #         @module Test3
    #         {
    #           void test2(@!(int)[Test2 test2 :(float)[Test1.toto]]);
    #         }
    #         """).to_c())
    #     self.assertEqual(res,
    #                     "")

if __name__ == "__main__":
    unittest.main()
