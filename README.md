# OpenVPN Management Interface Python API

[![Build Status](https://travis-ci.org/Jamie-/openvpn-api.svg?branch=master)](https://travis-ci.org/Jamie-/openvpn-api)
[![PyPI](https://img.shields.io/pypi/v/openvpn-api.svg)](https://pypi.org/project/openvpn-api/)

## Summary

A Python API for interacting with the OpenVPN management interface.
Currently a work in progress so support for client management interfaces and events is lacking.

Very useful for extracting metrics and status from OpenVPN server management interfaces.

This project was inspired by the work of Marcus Furlong in creating [openvpn-monitor](https://github.com/furlongm/openvpn-monitor).
It also uses [openvpn-status](https://pypi.org/project/openvpn-status/) by Jiangge Zhang for parsing the output of the OpenVPN `status` command as there's no point reinventing the wheel when an excellent solution already exists.

Release notes can be found [here on GitHub](https://github.com/Jamie-/openvpn-api/releases).

## Requirements
This project requires Python >= 3.6.

Other packages:
* [netaddr](https://pypi.org/project/netaddr/)
* [openvpn-status](https://pypi.org/project/openvpn-status/)

## Installation

#### Via PyPI
```
pip install openvpn-api
```

#### Via Source
```
git clone https://github.com/Jamie-/openvpn-api.git
cd openvpn-api
python setup.py install
```

## Usage

### Introduction
Create a `VPN` object for your management interface connection.
```python
import openvpn_api.VPN
v = openvpn_api.VPN('localhost', 7505)
```

Then you can either manage connection and disconnection yourself
```python
v.connect()
# Do some stuff, e.g.
print(v.release)
v.disconnect()
```
If the connection is successful, `v.connect()` will return `True`.
However, if the connection fails `v.connect()` will raise an `openvpn_api.errors.ConnectError` exception with the reason for the connection failure.

Or use the connection context manager
```python
with v.connection():
    # Do some stuff, e.g.
    print(v.release)
```

After initialising a VPN object, we can query specifics about it.

We can get the address we're communicating to the management interface on
```python
>>> v.mgmt_address
'localhost:7505'
```

And also see if this is via TCP/IP or a Unix socket
```python
>>> v.type
'ip'
```

or
```python
>>> v.type
'socket'
```

These are represented by the `VPNType` class as `VPNType.IP` or `VPNType.UNIX_SOCKET`
```python
>>> v.type
'ip'
>>> v.type == openvpn_api.VPNType.IP
True
```

### Daemon Interaction
All the properties that get information about the OpenVPN service you're connected to are stateful.
The first time you call one of these methods it caches the information it needs so future calls are super fast.
The information cached is unlikely to change often, unlike the status and metrics we can also fetch which are likely to change very frequently.

We can fetch the release string for the version of OpenVPN we're using
```python
>>> v.release
'OpenVPN 2.4.4 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018'
```

Or just the version number
```python
>>> v.version
'2.4.4'
```

We can get more information about the service by looking at it's state which is returned as a State object
```python
>>> s = v.state
>>> s
<models.state.State object at 0x7f5eb549a630>
```

The state cached by all 3 of these properties can be also be cleared and will be repopulated on the next call
```python
v.clear_cache()
```

#### Daemon State
The State object contains the following things:

The daemon's current mode, `client` or `server`
```python
>>> s.mode
'server'
```

Date and time the daemon was started
```python
>>> s.up_since
datetime.datetime(2019, 6, 5, 23, 3, 21)
```

The daemon's current state
```python
>>> s.state_name
'CONNECTED'
```
Which can be any of:
* `CONNECTING` - OpenVPN's initial state.
* `WAIT` - (Client only) Waiting for initial response from server.
* `AUTH` - (Client only) Authenticating with server.
* `GET_CONFIG` - (Client only) Downloading configuration options from server.
* `ASSIGN_IP` - Assigning IP address to virtual network interface.
* `ADD_ROUTES` - Adding routes to system.
* `CONNECTED` - Initialization Sequence Completed.
* `RECONNECTING` - A restart has occurred.
* `EXITING` - A graceful exit is in progress.
* `RESOLVE` - (Client only) DNS lookup
* `TCP_CONNECT` - (Client only) Connecting to TCP server

The descriptive string - unclear from the OpenVPN documentation quite what this is, usually `SUCCESS` or the reason for disconnection if the state is `RECONNECTING` or `EXITING`
```python
>>> s.desc_string
'SUCCESS'
```

The daemon's local virtual (VPN internal) address, returned as a `netaddr.IPAddress` for ease of sorting, it can be easily converted to a string with `str()`
```python
>>> s.local_virtual_v4_addr
IPAddress('10.0.0.1')
>>> str(s.local_virtual_v4_addr)
'10.0.0.1'
```

If the daemon is in client mode, then `remote_addr` and `remote_port` will be populated with the address and port of the remote server
```python
>>> s.remote_addr
'1.2.3.4'
>>> s.remote_port
1194
```

If the daemon is in server mode, then `local_addr` and `local_port` will be populated with the address and port of the exposed server
```python
>>> s.local_addr
'5.6.7.8'
>>> s.local_port
1194
```

If the daemon is using IPv6 instead of, or in addition to, IPv4 then the there is also a field for the local virtual (VPN internal) v6 address
```python
>>> s.local_virtual_v6_addr
'2001:db8:85a3::8a2e:370:7334'
```

#### Daemon Status
The daemon status is parsed from the management interface by `openvpn_status` an existing Python library for parsing the output from OpenVPN's status response.
The code for which can be found in it's GitHub repo: https://github.com/tonyseek/openvpn-status

Therefore when we fetch the status from the OpenVPN daemon, it'll be returned using their models.
For more information see their docs: https://openvpn-status.readthedocs.io/en/latest/api.html

Unlike the VPN state, the status is not stateful as it's output is highly likely to change between calls.
Every time the status is requested, the management interface is queried for the latest data.

A brief example:
```python
>>> status = v.get_status()
>>> status
<openvpn_status.models.Status object at 0x7f5eb54a2d68>
>>> status.client_list
OrderedDict([('1.2.3.4:56789', <openvpn_status.models.Client object at 0x7f5eb54a2128>)])
```
