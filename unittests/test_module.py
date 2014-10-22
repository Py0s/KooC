#!/usr/bin/env python3

import unittest
from KoocGrammar import Module
from KoocGrammar import KoocG
from cnorm.passes import to_c

class UnittestModule(unittest.TestCase):

    def setUp(self):
        self.cparse = KoocG()

    def test_empty_module(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
            }
            """).to_c())
        self.assertEqual(res,
                         "")
    def test_simple_declaration_variable(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             void test;
            }
            """).to_c())
        self.assertEqual(res,
                         "")
    def test_simple_declaration_assignement_variable(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             int test = 42;
            }
            """).to_c())
        self.assertEqual(res,
                         "")
    def test_simple_declaration_function(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             void test();
            }
            """).to_c())
        self.assertEqual(res,
                         "")
    def test_declaration_function(self):
        res = str(self.cparse.parse(
            """
            @module Test
            {
             char *test(int **toto, float tata[]);
            }
            """).to_c())
        self.assertEqual(res,
                        "")

    ## TODO : A mettre dans implementation
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
