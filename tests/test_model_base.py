import unittest
from openvpn_api.models import VPNModelBase

import netaddr  # type: ignore


class ModelStub(VPNModelBase):
    def parse_raw(cls, raw: str):
        return None


class TestModelBase(unittest.TestCase):
    def test_parse_string(self):
        self.assertIsNone(ModelStub._parse_string(None))
        self.assertIsNone(ModelStub._parse_string(""))
        self.assertEqual(ModelStub._parse_string("a"), "a")
        self.assertEqual(ModelStub._parse_string(" a "), "a")
        self.assertEqual(ModelStub._parse_string(1), "1")
        self.assertEqual(ModelStub._parse_string(False), "False")

    def test_parse_int(self):
        self.assertIsNone(ModelStub._parse_int(None))
        self.assertEqual(ModelStub._parse_int(0), 0)
        self.assertEqual(ModelStub._parse_int(1), 1)
        with self.assertRaises(ValueError):
            ModelStub._parse_int("a")
        with self.assertRaises(ValueError):
            ModelStub._parse_int(False)

    def test_parse_ipv4(self):
        self.assertIsNone(ModelStub._parse_ipv4(None))
        self.assertEqual(netaddr.IPAddress("1.2.3.4"), ModelStub._parse_ipv4("1.2.3.4"))
        self.assertEqual(netaddr.IPAddress("1.2.3.4"), ModelStub._parse_ipv4("  1.2.3.4  "))
        self.assertEqual(netaddr.IPAddress("1.2.3.4"), ModelStub._parse_ipv4("1.2.3.4\n"))
        with self.assertRaises(netaddr.core.AddrFormatError):
            ModelStub._parse_ipv4("asd")
