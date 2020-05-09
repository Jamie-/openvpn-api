import re
from typing import List, Dict

from openvpn_api.util import errors

EVENT_TYPE_REGEXES = {
    "CONNECT": re.compile(r"^>CLIENT:CONNECT,(?P<CID>([^,]+)),(?P<KID>([^,]+))$"),
    "REAUTH": re.compile(r"^>CLIENT:REAUTH,(?P<CID>([^,]+)),(?P<KID>([^,]+))$"),
    "ESTABLISHED": re.compile(r"^>CLIENT:ESTABLISHED,(?P<CID>([^,]+))$"),
    "DISCONNECT": re.compile(r"^>CLIENT:DISCONNECT,(?P<CID>([^,]+))$"),
    "ADDRESS": re.compile(r"^>CLIENT:ADDRESS,(?P<CID>([^,]+)),(?P<ADDR>([^,]+)),(?P<PRI>([^,]+))$"),
}

FIRST_LINE_REGEX = re.compile(r"^>CLIENT:(?P<event>([^,]+))(.*)$")
ENV_REGEX = re.compile(r">CLIENT:ENV,(?P<key>([^=]+))=(?P<value>(.+))")


class ClientEvent:
    def __init__(self, event_type, cid=None, kid=None, pri=None, addr=None, environment: Dict[str, str] = dict):
        self.type = event_type
        self.cid = int(cid) if cid is not None else None
        self.kid = int(kid) if kid is not None else None
        self.pri = int(pri) if pri is not None else None
        self.addr = int(addr) if addr is not None else None
        self.environment = environment


def is_input_began(line: str) -> bool:
    if not line:
        return False

    match = FIRST_LINE_REGEX.match(line)
    if not match:
        return False

    event_type = match.group("event")
    if event_type not in EVENT_TYPE_REGEXES:
        return False

    return True


def is_input_ended(line: str) -> bool:
    return line and (line.strip().startswith(">CLIENT:ADDRESS,") or line.strip() == ">CLIENT:ENV,END")


def parse_raw(lines: List[str]) -> "ClientEvent":
    if not lines:
        raise errors.ParseError("Event raw input is empty.")

    first_line = lines.pop(0)
    match = FIRST_LINE_REGEX.match(first_line)

    if not match:
        raise errors.ParseError("Syntax error in first line of client event (Line: %s)" % first_line)

    event_type = match.group("event")

    if event_type not in EVENT_TYPE_REGEXES:
        raise errors.ParseError(
            "This event type (%s) is not supported (Supported events: %s)" % (event_type, EVENT_TYPE_REGEXES)
        )

    match = EVENT_TYPE_REGEXES[event_type].match(first_line)

    if not match:
        raise errors.ParseError("Syntax error in first line of client event (Line: %s)" % first_line)

    first_line_data = match.groupdict()
    cid = int(first_line_data["CID"]) if "CID" in first_line_data else None
    kid = int(first_line_data["KID"]) if "KID" in first_line_data else None
    pri = int(first_line_data["KID"]) if "KID" in first_line_data else None
    addr = int(first_line_data["ADDR"]) if "ADDR" in first_line_data else None
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

    return ClientEvent(event_type=event_type, cid=cid, kid=kid, pri=pri, addr=addr, environment=environment)
