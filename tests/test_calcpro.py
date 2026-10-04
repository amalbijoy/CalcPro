import math
import unittest

from CalcPro import safe_eval


class SafeEvalTests(unittest.TestCase):
    def setUp(self):
        self.names = {
            "sqrt": math.sqrt,
            "abs": abs,
            "pi": math.pi,
        }

    def test_basic_expression(self):
        self.assertEqual(safe_eval("2 + 3 * 4", self.names), 14)

    def test_allowed_function(self):
        self.assertEqual(safe_eval("sqrt(16)", self.names), 4)

    def test_unknown_name_is_rejected(self):
        with self.assertRaises(NameError):
            safe_eval("unknown(1)", self.names)

    def test_unsupported_syntax_is_rejected(self):
        with self.assertRaises(ValueError):
            safe_eval("[1, 2, 3]", self.names)

    def test_very_long_expression_is_rejected(self):
        with self.assertRaises(ValueError):
            safe_eval("1+" * 300, self.names)


if __name__ == "__main__":
    unittest.main()
