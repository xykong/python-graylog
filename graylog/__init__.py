#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""graypy
Python logging handlers that send messages in the
Graylog Extended Log Format (GELF).
Modules:
 + :mod:`.http` - HTTP GELF Logging Handlers
 + :mod:`.tcp` - TCP GELF Logging Handler
 + :mod:`.tls` - TLS GELF Logging Handler
 + :mod:`.udp` - UDP GELF Logging Handler
"""

from graylog.handlers import (
    WAN_CHUNK,
    LAN_CHUNK,
)
from graylog.http import GELFHTTPHandler
from graylog.tcp import GELFTCPHandler
from graylog.tls import GELFTLSHandler
from graylog.udp import GELFUDPHandler

__version__ = (0, 3, 0)
