import unittest
import datetime
from unittest.mock import patch, PropertyMock
from openvpn_api.vpn import VPN, VPNType
from openvpn_api.util.errors import VPNError, ParseError


class TestVPNModel(unittest.TestCase):
    """Test the config file parser monitor.util.config_parser.ConfigParser
    """

    def test_host_port_socket(self):
        with self.assertRaises(VPNError) as ctx:
            VPN(host='localhost', port=1234, socket='file.sock')
        self.assertEqual('Must specify either socket or host and port', str(ctx.exception))

    def test_host_port(self):
        vpn = VPN(host='localhost', port=1234)
        self.assertEqual(vpn._mgmt_host, 'localhost')
        self.assertEqual(vpn._mgmt_port, 1234)
        self.assertIsNone(vpn._mgmt_socket)
        self.assertEqual(vpn.type, VPNType.IP)
        self.assertEqual(vpn.mgmt_address, 'localhost:1234')

    def test_socket(self):
        vpn = VPN(socket='file.sock')
        self.assertEqual(vpn._mgmt_socket, 'file.sock')
        self.assertIsNone(vpn._mgmt_host)
        self.assertIsNone(vpn._mgmt_port)
        self.assertEqual(vpn.type, VPNType.UNIX_SOCKET)
        self.assertEqual(vpn.mgmt_address, 'file.sock')

    def test_anchor(self):
        vpn = VPN(host='localhost', port=1234)
        vpn.name = 'Test VPN'
        self.assertEqual(vpn.anchor, 'test_vpn')
        vpn.name = 'asd_asd'
        self.assertEqual(vpn.anchor, 'asd_asd')

    @patch('openvpn_api.vpn.VPN.send_command')
    def test__get_version(self, mock_send_command):
        vpn = VPN(host='localhost', port=1234)
        mock_send_command.return_value = """
OpenVPN Version: OpenVPN 2.4.4 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018
Management Version: 1
END
        """
        self.assertEqual(vpn._get_version(),
                         'OpenVPN 2.4.4 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018')
        mock_send_command.assert_called_once_with('version')
        mock_send_command.reset_mock()
        mock_send_command.return_value = ""
        with self.assertRaises(ParseError) as ctx:
            vpn._get_version()
        self.assertEqual('Unable to get OpenVPN version, no matches found in socket response.', str(ctx.exception))
        mock_send_command.assert_called_once_with('version')
        mock_send_command.reset_mock()
        mock_send_command.return_value = """
Management Version: 1
END
        """
        with self.assertRaises(ParseError) as ctx:
            vpn._get_version()
        self.assertEqual('Unable to get OpenVPN version, no matches found in socket response.', str(ctx.exception))
        mock_send_command.assert_called_once_with('version')
        mock_send_command.reset_mock()

    @patch('openvpn_api.vpn.VPN._get_version')
    def test_release(self, mock_get_version):
        vpn = VPN(host='localhost', port=1234)
        self.assertIsNone(vpn._release)
        release_string = 'OpenVPN 2.4.4 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018'
        mock_get_version.return_value = release_string
        self.assertEqual(vpn.release, release_string)
        self.assertEqual(vpn._release, release_string)
        mock_get_version.assert_called_once_with()
        mock_get_version.reset_mock()
        vpn._release = 'asd'
        self.assertEqual(vpn.release, 'asd')
        mock_get_version.assert_not_called()

    @patch('openvpn_api.vpn.VPN._get_version')
    def test_version(self, mock_get_version):
        vpn = VPN(host='localhost', port=1234)
        vpn._release = 'OpenVPN 2.4.4 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018'
        self.assertEqual(vpn.version, '2.4.4')
        vpn._release = 'OpenVPN 1.2.3 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018'
        self.assertEqual(vpn.version, '1.2.3')
        vpn._release = 'OpenVPN 11.22.33 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018'
        self.assertEqual(vpn.version, '11.22.33')
        vpn._release = None
        mock_get_version.assert_not_called()  # Check mock hasn't been triggered up to this point
        mock_get_version.return_value = None
        self.assertIsNone(vpn.version)
        mock_get_version.assert_called_once()
        mock_get_version.reset_mock()
        vpn._release = 'asd'
        with self.assertRaises(ParseError) as ctx:
            vpn.version()
        self.assertEqual('Unable to parse version from release string.', str(ctx.exception))
        mock_get_version.assert_not_called()

    @patch('openvpn_api.vpn.VPN.send_command')
    def test_server_state(self, mock):
        vpn = VPN(host='localhost', port=1234)
        mock.return_value = """1560719601,CONNECTED,SUCCESS,10.0.0.1,,,1.2.3.4,1194
END"""
        self.assertIsNone(vpn._state)
        state = vpn.state
        mock.assert_called_once()
        self.assertEqual(datetime.datetime(2019, 6, 16, 21, 13, 21), state.up_since)
        self.assertEqual('CONNECTED', state.state_name)
        self.assertEqual('SUCCESS', state.desc_string)
        self.assertEqual('10.0.0.1', state.local_virtual_v4_addr)
        self.assertIsNone(state.remote_addr)
        self.assertIsNone(state.remote_port)
        self.assertEqual('1.2.3.4', state.local_addr)
        self.assertEqual(1194, state.local_port)
        mock.reset_mock()
        _ = vpn.state
        mock.assert_not_called()

    @patch('openvpn_api.vpn.VPN.release', new_callable=PropertyMock)
    @patch('openvpn_api.vpn.VPN.state', new_callable=PropertyMock)
    def test_cache(self, release_mock, state_mock):
        """Test caching VPN metadata works and clears correctly.
        """
        vpn = VPN(host='localhost', port=1234)
        vpn.cache_data()
        release_mock.assert_called_once()
        state_mock.assert_called_once()
        vpn._release = 'asd'
        vpn._state = 'qwe'
        vpn.clear_cache()
        self.assertIsNone(vpn._release)
        self.assertIsNone(vpn._state)

    @patch('openvpn_api.vpn.VPN.send_command')
    def test_get_stats(self, mock):
        # Normal response from send_command
        vpn = VPN(host='localhost', port=1234)
        mock.return_value = "SUCCESS: nclients=3,bytesin=129822996,bytesout=126946564\n"
        stats = vpn.get_stats()
        mock.assert_called_once()
        self.assertEqual(3, stats.client_count)
        self.assertEqual(129822996, stats.bytes_in)
        self.assertEqual(126946564, stats.bytes_out)
        mock.reset_mock()
        # Blank response from send_command
        mock.return_value = ""
        with self.assertRaises(ParseError) as ctx:
            vpn.get_stats()
        self.assertEqual('Did not get expected response from load-stats.', str(ctx.exception))
        mock.assert_called_once()
        mock.reset_mock()
        # Bad response from send_command
        mock.return_value = "SUCCESS: nclients=3\n"
        with self.assertRaises(ParseError) as ctx:
            vpn.get_stats()
        self.assertEqual('Unable to parse stats from load-stats response.', str(ctx.exception))
        mock.assert_called_once()
