import unittest

from openvpn_api.events import client as ClientEvent
from openvpn_api.util import errors


class TestEventClient(unittest.TestCase):
    def test_input_began(self):
        self.assertTrue(ClientEvent.is_input_began(">CLIENT:CONNECT,14,23,"))

    def test_input_not_began(self):
        self.assertFalse(ClientEvent.is_input_began(">BYTES:14,23"))

    def test_input_not_began_invalid_type(self):
        self.assertFalse(ClientEvent.is_input_began(">CLIENT:INVALID-TYPE,14,23,"))

    def test_input_not_began_empty_input(self):
        self.assertFalse(ClientEvent.is_input_began(""))

    def test_input_ended_normal(self):
        self.assertTrue(ClientEvent.is_input_ended(">CLIENT:ENV,END"))

    def test_input_ended_one_liner(self):
        self.assertTrue(ClientEvent.is_input_ended(">CLIENT:ADDRESS,14,3,1.1.1.1"))

    def test_empty_lines(self):
        with self.assertRaises(errors.ParseError) as ctx:
            ClientEvent.parse_raw([])
        self.assertEqual("Event raw input is empty.", str(ctx.exception))

    def test_deserialize_connect_event(self):
        event = ClientEvent.parse_raw(
            [
                ">CLIENT:CONNECT,14,43",
                ">CLIENT:ENV,common_name=test_cn",
                ">CLIENT:ENV,time_unix=12343212343",
                ">CLIENT:ENV,END",
            ]
        )
        self.assertEqual("CONNECT", event.type)
        self.assertEqual(14, event.cid)
        self.assertEqual(43, event.kid)
        self.assertEqual({"common_name": "test_cn", "time_unix": "12343212343"}, event.environment)

    def test_deserialize_reauth_event(self):
        event = ClientEvent.parse_raw(
            [
                ">CLIENT:REAUTH,14,43",
                ">CLIENT:ENV,common_name=test_cn",
                ">CLIENT:ENV,time_unix=12343212343",
                ">CLIENT:ENV,END",
            ]
        )
        self.assertEqual("REAUTH", event.type)
        self.assertEqual(14, event.cid)
        self.assertEqual(43, event.kid)
        self.assertEqual({"common_name": "test_cn", "time_unix": "12343212343"}, event.environment)

    def test_deserialize_established_event(self):
        event = ClientEvent.parse_raw(
            [
                ">CLIENT:ESTABLISHED,14",
                ">CLIENT:ENV,common_name=test_cn",
                ">CLIENT:ENV,time_unix=12343212343",
                ">CLIENT:ENV,END",
            ]
        )
        self.assertEqual("ESTABLISHED", event.type)
        self.assertEqual(14, event.cid)
        self.assertEqual({"common_name": "test_cn", "time_unix": "12343212343"}, event.environment)

    def test_deserialize_disconnect_event(self):
        event = ClientEvent.parse_raw(
            [
                ">CLIENT:DISCONNECT,14",
                ">CLIENT:ENV,common_name=test_cn",
                ">CLIENT:ENV,time_unix=12343212343",
                ">CLIENT:ENV,END",
            ]
        )
        self.assertEqual("DISCONNECT", event.type)
        self.assertEqual(14, event.cid)
        self.assertEqual({"common_name": "test_cn", "time_unix": "12343212343"}, event.environment)

    def test_empty_environment(self):
        with self.assertRaises(errors.ParseError) as ctx:
            a = ClientEvent.parse_raw([">CLIENT:DISCONNECT,14", ">CLIENT:ENV,END",])

        self.assertEqual("This event type (DISCONNECT) doesn't support empty environment.", str(ctx.exception))

    def test_missing_environment(self):
        with self.assertRaises(errors.ParseError) as ctx:
            ClientEvent.parse_raw(
                [">CLIENT:DISCONNECT,14",]
            )

        self.assertEqual("The raw event doesn't have an >CLIENT:ENV,END line.", str(ctx.exception))

    def test_invalid_type(self):
        with self.assertRaises(errors.ParseError) as ctx:
            ClientEvent.parse_raw(
                [">CLIENT:NOT-SUPPORTED,14",]
            )

        self.assertEqual(
            "This event type (NOT-SUPPORTED) is not supported (Supported events: %s)"
            % (ClientEvent.EVENT_TYPE_REGEXES),
            str(ctx.exception),
        )
