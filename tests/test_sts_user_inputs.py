"""Unit test module for sts_ux"""

import unittest
from unittest.mock import patch
from sts_user_inputs import int_validation, yn_validation, string_validation


@patch("sts_user_inputs.input")
class TestUiIntValidation(unittest.TestCase):
    """Contains unit tests for the int validation helper function"""

    def test_valid_inputs(self, mock_get_alpha):
        """Tests helper returns valid input"""

        mock_get_alpha.return_value = "5"
        self.assertEqual(int_validation("test", min_value=1, max_value=10), 5)

        mock_get_alpha.return_value = "5"
        self.assertEqual(int_validation("test", min_value=5, max_value=5), 5)

        mock_get_alpha.return_value = "13"
        self.assertEqual(int_validation("test", min_value=1, max_value=20), 13)

        mock_get_alpha.return_value = "20"
        self.assertEqual(int_validation("test", min_value=1, max_value=20), 20)

        mock_get_alpha.return_value = "1"
        self.assertEqual(int_validation("test", min_value=1, max_value=20), 1)

        mock_get_alpha.return_value = "3 "
        self.assertEqual(int_validation("test", min_value=-8, max_value=5), 3)

        mock_get_alpha.return_value = " 3 "
        self.assertEqual(int_validation("test", min_value=-8, max_value=5), 3)

        mock_get_alpha.return_value = " 3"
        self.assertEqual(int_validation("test", min_value=-8, max_value=5), 3)

    def test_neg_inputs(self, mock_get_alpha):
        """Tests function handles negative inputs correctly"""

        mock_get_alpha.return_value = "-5"
        self.assertEqual(int_validation("test", min_value=-8, max_value=5), -5)

        mock_get_alpha.return_value = "-5"
        self.assertFalse(int_validation("test", min_value=0, max_value=5))

    def test_floats(self, mock_get_alpha):
        """Tests function handles decimal inputs correctly"""

        mock_get_alpha.return_value = "4.0"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "3.7"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "12.0"
        self.assertFalse(int_validation("test", min_value=1, max_value=10))

        mock_get_alpha.return_value = "7.3"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

    def test_non_numeric_inputs(self, mock_get_alpha):
        """Tests function handles non-numeric inputs correctly"""

        mock_get_alpha.return_value = ""
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = " "
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "          "
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "f"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "foo"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "foo bar baz"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "3b"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))

        mock_get_alpha.return_value = "!"
        self.assertFalse(int_validation("test", min_value=1, max_value=6))


@patch("sts_user_inputs.input")
class TestUiYNValidation(unittest.TestCase):
    """Contains numerous unit tests for the y/N validation helper function"""

    def test_valid_inputs(self, mock_get_alpha):
        """Tests helper returns valid input"""

        mock_get_alpha.return_value = "y"
        self.assertEqual(yn_validation("test"), "y")

        mock_get_alpha.return_value = " y"
        self.assertEqual(yn_validation("test"), "y")

        mock_get_alpha.return_value = "Y"
        self.assertEqual(yn_validation("test"), "y")

        mock_get_alpha.return_value = "Y "
        self.assertEqual(yn_validation("test"), "y")

        mock_get_alpha.return_value = "n"
        self.assertEqual(yn_validation("test"), "n")

        mock_get_alpha.return_value = "    n       "
        self.assertEqual(yn_validation("test"), "n")

        mock_get_alpha.return_value = "N"
        self.assertEqual(yn_validation("test"), "n")

        mock_get_alpha.return_value = "yes"
        self.assertEqual(yn_validation("test"), "yes")

        mock_get_alpha.return_value = "Yes"
        self.assertEqual(yn_validation("test"), "yes")

        mock_get_alpha.return_value = "YES"
        self.assertEqual(yn_validation("test"), "yes")

        mock_get_alpha.return_value = "             YES"
        self.assertEqual(yn_validation("test"), "yes")

        mock_get_alpha.return_value = "no"
        self.assertEqual(yn_validation("test"), "no")

        mock_get_alpha.return_value = "No"
        self.assertEqual(yn_validation("test"), "no")

        mock_get_alpha.return_value = "NO"
        self.assertEqual(yn_validation("test"), "no")

    def test_invalid_inputs(self, mock_get_alpha):
        """Tests helper handles invalid inputs"""

        mock_get_alpha.return_value = "x"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "F"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "foo"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "BAR"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "True"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "False"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = " "
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "      "
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "!"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "y3s"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "0"
        self.assertFalse(yn_validation("test"))

        mock_get_alpha.return_value = "3"
        self.assertFalse(yn_validation("test"))


@patch("sts_user_inputs.input")
class TestUiStringValidation(unittest.TestCase):
    """Contains unit tests for the string validation helper function"""

    def test_valid_inputs(self, mock_get_alpha):
        """Tests helper handles and returns valid inputs"""

        mock_get_alpha.return_value = "Hello World"
        self.assertEqual(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=True),
            "Hello World",
        )

        mock_get_alpha.return_value = "username"
        self.assertEqual(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=False),
            "username",
        )

        mock_get_alpha.return_value = "1234"
        self.assertEqual(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=True),
            "1234",
        )

        mock_get_alpha.return_value = "Foo 1 bar 2 BAZ 345"
        self.assertEqual(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=True),
            "Foo 1 bar 2 BAZ 345",
        )

        mock_get_alpha.return_value = "Foo"
        self.assertEqual(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=True),
            "Foo",
        )

        mock_get_alpha.return_value = " bar "
        self.assertEqual(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=False),
            "bar",
        )

        mock_get_alpha.return_value = "foo"
        self.assertEqual(
            string_validation("test", max_len=5, min_len=1, alpha=False, spaces=False),
            "foo",
        )

        mock_get_alpha.return_value = "foo"
        self.assertEqual(
            string_validation("test", max_len=3, min_len=1, alpha=False, spaces=False),
            "foo",
        )

        mock_get_alpha.return_value = "foobarbaz"
        self.assertEqual(
            string_validation("test", max_len=9, min_len=9, alpha=False, spaces=False),
            "foobarbaz",
        )

        mock_get_alpha.return_value = "foo bar baz"
        self.assertEqual(
            string_validation("test", max_len=0, min_len=5, alpha=True, spaces=True),
            "foo bar baz",
        )

    def test_invalid_inputs_alpha_false(self, mock_get_alpha):
        """Tests helper handles and returns valid inputs"""

        # input > max_length
        mock_get_alpha.return_value = "Hello World"
        self.assertFalse(
            string_validation("test", max_len=10, min_len=1, alpha=False, spaces=True)
        )

        # input includes spaces
        mock_get_alpha.return_value = "Hello World"
        self.assertFalse(
            string_validation("test", max_len=10, min_len=1, alpha=False, spaces=False)
        )

        # input < min_length
        mock_get_alpha.return_value = "Hello World"
        self.assertFalse(
            string_validation("test", max_len=0, min_len=15, alpha=False, spaces=True)
        )

        # input > min_length && max_length
        mock_get_alpha.return_value = "Hello World"
        self.assertFalse(
            string_validation("test", max_len=8, min_len=8, alpha=False, spaces=True)
        )

        # alpha=True & input numerical
        mock_get_alpha.return_value = "1234"
        self.assertFalse(
            string_validation("test", max_len=0, min_len=1, alpha=True, spaces=True)
        )

        # alpha=True & input containing a number
        mock_get_alpha.return_value = "foo 1"
        self.assertFalse(
            string_validation("test", max_len=0, min_len=1, alpha=True, spaces=True)
        )

        # alpha=True & input containing '!'
        mock_get_alpha.return_value = "foo!"
        self.assertFalse(
            string_validation("test", max_len=0, min_len=1, alpha=True, spaces=True)
        )

        # input = spaces, returns '' i.e. False
        mock_get_alpha.return_value = "  "
        self.assertFalse(
            string_validation("test", max_len=0, min_len=1, alpha=True, spaces=False)
        )

        # input = '   ', returns '' i.e. False - alpha=False
        mock_get_alpha.return_value = "  "
        self.assertFalse(
            string_validation("test", max_len=0, min_len=1, alpha=False, spaces=False)
        )


if __name__ == "__main__":
    unittest.main()
