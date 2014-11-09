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


#     def test_simple_function_call(self):
#         res = str(self.kparse.parse(
#             """
#             @module Test
#             {
#              int test(void);
#             }
#             int main()
#             {
#               [Test test];
#             }
#             """).to_c())
#         waited = str(self.cparse.parse("""
# extern int M4Test__i4testv(void);
# int main()
# {
#     M4Test__i4testv();
# }
#             """).to_c())
#         self.assertEqual(res, waited)

    def test_simple_variable_call(self):
        res = str(self.kparse.parse(
            """
            @module Test
            {
             int test;
            }
            int main()
            {
              [Test.test];
            }
            """).to_c())
        waited = str(self.cparse.parse("""
extern int M4Test__i4test;
int main()
{
    M4Test__i4test;
}
            """).to_c())
        print("RESULT = ", res, "\n")
        print("WAITED = ", waited, "\n")
        self.assertEqual(res, waited)


    # def test_simple_variable_call(self):
    #     res = self.kparse.parse(
    #         """
    #         int main()
    #         {
    #           [Test.test];
    #         }
    #         """)
    #     print(res.diagnostic.get_content())
    #     waited = str(self.cparse.parse("""
    # M4Test__i4test;
    #         """).to_c())
    #     print("RESULT = ", res, "\n")
    #     print("WAITED = ", waited, "\n")
    #     self.assertEqual(res, waited)


#     def test_simple_variable_assign_call(self):
#         res = str(self.kparse.parse(
#             """
#             @module Test
#             {
#              int test;
#             }
#             int main()
#             {
#               int a = [Test.test];
#             }
#             """).to_c())
#         waited = str(self.cparse.parse("""
# extern int M4Test__i4test;
# int main()
# {
#     int a = M4Test__i4test;
# }
#             """).to_c())
#         self.assertEqual(res, waited)
#     def test_simple_function_arg_call(self):
#         res = str(self.kparse.parse(
#             """
#             @module Test
#             {
#              int test(int toto);
#             }
#             int main()
#             {
#               [Test test :(int)42];
#             }
#             """).to_c())
#         waited = str(self.cparse.parse("""
# extern int M4Test__i4testi(int toto);
# int main()
# {
#     M4Test__i4testi(42);
# }
#             """).to_c())
#         self.assertEqual(res, waited)










    # def test_koocCall_in_function(self):
    #     res = str(self.cparse.parse(
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
    #     res = str(self.cparse.parse(
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
    #     res = str(self.cparse.parse(
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
