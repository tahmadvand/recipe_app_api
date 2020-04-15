# ## CREATE A BASIC UNITTEST##
#
# from django.test import TestCase
# # is a class that comes with Django that basically
# # has a bunch of helper functions that help us test our django code.
#
# from .calc import add, subtract
#
#
# class CalcTests(TestCase):
#
#     def test_add_numbers(self):
#         # just like when Django searches for the files that begin with test, the test
#         # functions must all begin with tests
#         """Test that values are added together"""
#         self.assertEqual(add(3, 8), 11)
#         ## there's the assertion which is when you actually test the output and
#         # you confirm that the output equals what you expected it to equal.
#
#     def test_subtract_numbers(self):
#         """Test that values are subtracted and returned"""
#         self.assertEqual(subtract(5, 11), 6)