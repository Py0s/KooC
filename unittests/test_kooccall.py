#!/usr/bin/env python3

import unittest
from KoocGrammar import KoocG
from KoocGrammar import Module
from cnorm.passes import to_c
import KoocFile

class UnittestKooccall(unittest.TestCase):

    def setUp(self):
        self.cparse = KoocG()

    def tearDown(self):
        self.cparse = None
        KoocFile.debugCleanAll()


    def test_simple_function_call(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             int test(void);
            }
            int main()
            {
              [Test test];
            }
            """).to_c())
        waited = """
extern int M4Test__i4testv(void);
int main()
{
    M4Test__i4testv();
}
            """
        self.assertEqual(res, waited)
    def test_simple_variable_call(self):
        res = str(self.cparse.parse(
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
        waited = """
extern int M4Test__i4testv;
int main()
{
    M4Test__i4testv;
}
            """
        self.assertEqual(res, waited)
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
