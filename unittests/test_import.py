#!/usr/bin/env python3

import unittest
from KoocGrammar import Import
import KoocFile

class UnittestImport(unittest.TestCase):

	def setUp(self):
		KoocFile.includePath = "./test/import_test"

	# def test_import_infini(self):
	# 	self.assertTrue(KoocFile.kooc_a_file("import_infini.kh"))
#import infini, multiple
#appeler kooc_a_file sur les fichiers de test

if __name__ == "__main__":
    unittest.main()
