from unittest import TestCase


class TestForActions(TestCase):
    def test_addition(self):
        equation = 9 + 9
        expected = 18
        self.assertEqual(equation, expected)
