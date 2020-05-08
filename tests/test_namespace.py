import unittest


class TestNamespace(unittest.TestCase):
    def test_import(self):
        from openvpn_api import VPN
        from openvpn_api import VPNType
        from openvpn_api import errors
