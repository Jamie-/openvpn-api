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

    def test_parse_notification(self):
        self.assertEqual(("BYTECOUNT", "asd"), ModelStub._parse_notification(">BYTECOUNT:asd"))
        self.assertEqual(("CLIENT", "asd:qwe"), ModelStub._parse_notification(">CLIENT:asd:qwe"))
        with self.assertRaises(AssertionError):
            ModelStub._parse_notification(">INFO")
        self.assertEqual((None, None), ModelStub._parse_notification("asd"))

    def test_is_notification(self):
        self.assertTrue(ModelStub._is_notification(">BYTECOUNT:asd"))
        self.assertTrue(ModelStub._is_notification(">BYTECOUNT_CLI:asd"))
        self.assertTrue(ModelStub._is_notification(">CLIENT:asd"))
        self.assertTrue(ModelStub._is_notification(">ECHO:asd"))
        self.assertTrue(ModelStub._is_notification(">FATAL:asd"))
        self.assertTrue(ModelStub._is_notification(">HOLD:asd"))
        self.assertTrue(ModelStub._is_notification(">INFO:asd"))
        self.assertTrue(ModelStub._is_notification(">LOG:asd"))
        self.assertTrue(ModelStub._is_notification(">NEED-OK:asd"))
        self.assertTrue(ModelStub._is_notification(">NEED-STR:asd"))
        self.assertTrue(ModelStub._is_notification(">PASSWORD:asd"))
        self.assertTrue(ModelStub._is_notification(">STATE:asd"))
        self.assertTrue(ModelStub._is_notification(">REMOTE:asd"))
        self.assertTrue(ModelStub._is_notification(">PROXY:asd"))
        self.assertTrue(ModelStub._is_notification(">RSA_SIGN:asd"))
        self.assertFalse(ModelStub._is_notification(">XXX:asd"))
