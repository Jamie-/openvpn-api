import unittest
from ipaddress import IPv4Address, IPv6Address

from openvpn_api.util import parsing


class TestUtilParsing(unittest.TestCase):
    def test_parse_string(self):
        self.assertIsNone(parsing.parse_string(None))
        self.assertIsNone(parsing.parse_string(""))
        self.assertEqual(parsing.parse_string("a"), "a")
        self.assertEqual(parsing.parse_string(" a "), "a")
        self.assertEqual(parsing.parse_string(1), "1")
        self.assertEqual(parsing.parse_string(False), "False")

    def test_parse_int(self):
        self.assertIsNone(parsing.parse_int(None))
        self.assertEqual(parsing.parse_int(0), 0)
        self.assertEqual(parsing.parse_int(1), 1)
        with self.assertRaises(ValueError):
            parsing.parse_int("a")
        with self.assertRaises(ValueError):
            parsing.parse_int(False)

    def test_parse_ipaddress(self):
        self.assertIsNone(parsing.parse_ipaddress(None))
        with self.subTest("IPv4"):
            self.assertEqual(IPv4Address("1.2.3.4"), parsing.parse_ipaddress("1.2.3.4"))
            self.assertEqual(IPv4Address("1.2.3.4"), parsing.parse_ipaddress("  1.2.3.4  "))
            self.assertEqual(IPv4Address("1.2.3.4"), parsing.parse_ipaddress("1.2.3.4\n"))
        with self.subTest("IPv6"):
            self.assertEqual(IPv6Address("::1:2:3:4"), parsing.parse_ipaddress("::1:2:3:4"))
            self.assertEqual(IPv6Address("::1:2:3:4"), parsing.parse_ipaddress("  ::1:2:3:4  "))
            self.assertEqual(IPv6Address("::1:2:3:4"), parsing.parse_ipaddress("::1:2:3:4\n"))
        with self.assertRaises(ValueError):
            parsing.parse_ipaddress("asd")
