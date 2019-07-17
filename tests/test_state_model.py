import unittest
import datetime
import models.state


class TestState(unittest.TestCase):

    def test_init(self):
        s = models.state.State(
            '1560719601',
            'CONNECTED',
            'SUCCESS',
            '10.0.0.1',
            None,  # Should be None for server state
            None,  # Should be None for server state
            '1.2.3.4',
            '1194',
            None
        )
        self.assertEqual(datetime.datetime(2019, 6, 16, 22, 13, 21), s.up_since)
        self.assertEqual('CONNECTED', s.state_name)
        self.assertEqual('SUCCESS', s.desc_string)
        self.assertEqual('10.0.0.1', s.local_virtual_v4_addr)
        self.assertIsNone(s.remote_addr)
        self.assertIsNone(s.remote_port)
        self.assertEqual('1.2.3.4', s.local_addr)
        self.assertEqual(1194, s.local_port)
        self.assertIsNone(s.local_virtual_v6_addr)
        # Props
        self.assertEqual('server', s.mode)

    def test_init_none(self):
        s = models.state.State(None, None, None, None, None, None, None, None, None)
        self.assertIsNone(s.up_since)
        self.assertIsNone(s.state_name)
        self.assertIsNone(s.desc_string)
        self.assertIsNone(s.local_virtual_v4_addr)
        self.assertIsNone(s.remote_addr)
        self.assertIsNone(s.remote_port)
        self.assertIsNone(s.local_addr)
        self.assertIsNone(s.local_port)
        self.assertIsNone(s.local_virtual_v6_addr)
        # Props
        self.assertEqual('unknown', s.mode)
