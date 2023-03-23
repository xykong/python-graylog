#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""graypy
Python logging handlers that send messages in the
Graylog Extended Log Format (GELF).
Modules:
 + :mod:`.handler` - Basic GELF Logging Handlers
 + :mod:`.rabbitmq` - RabbitMQ GELF Logging Handler
"""

from graylog.handlers import (
    WAN_CHUNK,
    LAN_CHUNK,
)
from graylog.udp import GELFUDPHandler
from graylog.tcp import GELFTCPHandler
from graylog.tls import GELFTLSHandler
from graylog.http import GELFHTTPHandler

try:
    from graylog.rabbitmq import GELFRabbitHandler, ExcludeFilter
except ImportError:
    pass  # amqplib is probably not installed

__version__ = (2, 1, 0)
