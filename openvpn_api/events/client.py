import re
from typing import List, Dict, Optional

from openvpn_api.util import errors
from openvpn_api import events

FIRST_LINE_REGEX = re.compile(r"^>CLIENT:(?P<event>([^,]+))(.*)$")
ENV_REGEX = re.compile(r">CLIENT:ENV,(?P<key>([^=]+))=(?P<value>(.+))")


@events.register_event
class ClientEvent(events.BaseEvent):
    EVENT_TYPE_REGEXES = {
        "CONNECT": re.compile(r"^>CLIENT:CONNECT,(?P<client_id>([^,]+)),(?P<key_id>([^,]+))$"),
        "REAUTH": re.compile(r"^>CLIENT:REAUTH,(?P<client_id>([^,]+)),(?P<key_id>([^,]+))$"),
        "ESTABLISHED": re.compile(r"^>CLIENT:ESTABLISHED,(?P<client_id>([^,]+))$"),
        "DISCONNECT": re.compile(r"^>CLIENT:DISCONNECT,(?P<client_id>([^,]+))$"),
        "ADDRESS": re.compile(r"^>CLIENT:ADDRESS,(?P<client_id>([^,]+)),(?P<address>([^,]+)),(?P<primary>([^,]+))$"),
    }

    def __init__(
        self,
        event_type,
        client_id: int,
        key_id: Optional[int] = None,
        primary: Optional[int] = None,
        address=None,
        environment: Dict[str, str] = None,
    ):
        self.type = event_type
        self.client_id = client_id
        self.key_id = key_id
        self.primary = primary
        self.address = address
        self.environment = environment
        if self.environment is None:
            self.environment = {}

    @classmethod
    def has_begun(cls, line: str) -> bool:
        if not line:
            return False

        match = FIRST_LINE_REGEX.match(line)
        if not match:
            return False

        event_type = match.group("event")
        if event_type not in cls.EVENT_TYPE_REGEXES:
            return False

        return True

    @classmethod
    def has_ended(cls, line: str) -> bool:
        return line and (line.strip().startswith(">CLIENT:ADDRESS,") or line.strip() == ">CLIENT:ENV,END")

    @classmethod
    def parse_raw(cls, lines: List[str]) -> "ClientEvent":
        if not lines:
            raise errors.ParseError("Event raw input is empty.")

        first_line = lines.pop(0)
        match = FIRST_LINE_REGEX.match(first_line)

        if not match:
            raise errors.ParseError("Syntax error in first line of client event (Line: %s)" % first_line)

        event_type = match.group("event")

        if event_type not in cls.EVENT_TYPE_REGEXES:
            raise errors.ParseError(
                "This event type (%s) is not supported (Supported events: %s)" % (event_type, cls.EVENT_TYPE_REGEXES)
            )

        match = cls.EVENT_TYPE_REGEXES[event_type].match(first_line)

        if not match:
            raise errors.ParseError("Syntax error in first line of client event (Line: %s)" % first_line)

        first_line_data = match.groupdict()
        assert "client_id" in first_line_data, "unexpected CLIENT real-time message, cannot parse"
        client_id = int(first_line_data["client_id"])
        key_id = int(first_line_data["key_id"]) if "key_id" in first_line_data else None
        primary = int(first_line_data["key_id"]) if "key_id" in first_line_data else None
        address = int(first_line_data["address"]) if "address" in first_line_data else None
        environment = {}

        if event_type != "ADDRESS":

            for line in lines:
                if line.strip() == ">CLIENT:ENV,END":
                    break

                match = ENV_REGEX.match(line)
                if not match:
                    raise errors.ParseError("Invalid line in client event (Line: %s)" % line)

                environment[match.group("key")] = match.group("value")
            else:
                raise errors.ParseError("The raw event doesn't have an >CLIENT:ENV,END line.")

            if not environment:
                raise errors.ParseError("This event type (%s) doesn't support empty environment." % event_type)

        return ClientEvent(
            event_type=event_type,
            client_id=client_id,
            key_id=key_id,
            primary=primary,
            address=address,
            environment=environment,
        )
