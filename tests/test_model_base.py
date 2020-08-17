import unittest
from ipaddress import IPv4Address, IPv6Address

from openvpn_api.models import VPNModelBase


class ModelStub(VPNModelBase):
    def parse_raw(cls, raw: str):
        return None


class TestModelBase(unittest.TestCase):
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
