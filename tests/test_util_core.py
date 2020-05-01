import unittest
import openvpn_api.util as util


class TestUtilCore(unittest.TestCase):
    def test_nonify_string(self):
        self.assertIsNone(util.nonify_string(None))
        self.assertIsNone(util.nonify_string(""))
        self.assertEqual(util.nonify_string("a"), "a")
        self.assertEqual(util.nonify_string(1), "1")
        self.assertEqual(util.nonify_string(False), "False")

    def test_nonify_int(self):
        self.assertIsNone(util.nonify_int(None))
        self.assertEqual(util.nonify_int(0), 0)
        self.assertEqual(util.nonify_int(1), 1)
        with self.assertRaises(ValueError):
            util.nonify_int("a")
        with self.assertRaises(ValueError):
            util.nonify_int(False)
