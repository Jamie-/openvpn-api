import unittest
from openvpn_api.models import stats
from openvpn_api.util import errors


class TestServerStats(unittest.TestCase):
    def test_repr(self):
        s = stats.ServerStats(client_count=15, bytes_in=23984723, bytes_out=24532)
        self.assertEqual("<ServerStats client_count=15, bytes_in=23984723, bytes_out=24532>", repr(s))

    def test_parse_raw(self):
        s = stats.ServerStats.parse_raw("SUCCESS: nclients=3,bytesin=129822996,bytesout=126946564")
        self.assertEqual(3, s.client_count)
        self.assertEqual(129822996, s.bytes_in)
        self.assertEqual(126946564, s.bytes_out)

    def test_parse_raw_empty(self):
        with self.assertRaises(errors.ParseError) as ctx:
            stats.ServerStats.parse_raw("")
        self.assertEqual("Did not get expected data from load-stats.", str(ctx.exception))

    def test_parse_raw_invalid(self):
        with self.assertRaises(errors.ParseError) as ctx:
            stats.ServerStats.parse_raw("SUCCESS: nclients=3")
        self.assertEqual("Unable to parse stats from raw load-stats response.", str(ctx.exception))

    def test_parse_raw_prefix(self):
        s = stats.ServerStats.parse_raw(
            """
>INFO: asd
SUCCESS: nclients=3,bytesin=129822996,bytesout=126946564
"""
        )
        self.assertEqual(3, s.client_count)
        self.assertEqual(129822996, s.bytes_in)
        self.assertEqual(126946564, s.bytes_out)
