import sys 
import os
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "traindelay"))

from constants import Constants
import re
import unittest


class TestRegex(unittest.TestCase):

	def test_interface(self):
		# standard input
		user_input = r"yrk shf 0800 2020-10-09"
		self.assertEqual(re.search(Constants.interface_pattern, user_input).groups(), ("yrk", "shf", "0800", "2020-10-09"))
		
		# no match
		user_input = r"yrkk shff 0800 2020-10-09"
		self.assertEqual(re.search(Constants.interface_pattern, user_input), None)
		

if __name__ == '__main__':
	unittest.main()