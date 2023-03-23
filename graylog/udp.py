from logging.handlers import DatagramHandler

from graylog.handlers import BaseGELFHandler, GELFWarningChunker


class GELFUDPHandler(BaseGELFHandler, DatagramHandler):
    """GELF UDP handler"""

    def __init__(self, host, port=12202, gelf_chunker=GELFWarningChunker(), **kwargs):
        """Initialize the GELFUDPHandler

        .. note::
            By default a :class:`.handler.GELFWarningChunker` is used as the
            ``gelf_chunker``. Thus, GELF messages that chunk overflow will
            issue a :class:`.handler.GELFChunkOverflowWarning` and will be
            dropped.

        :param host: GELF UDP input host.
        :type host: str

        :param port: GELF UDP input port.
        :type port: int

        :param gelf_chunker: :class:`.handler.BaseGELFChunker` instance to
            handle chunking larger GELF messages.
        :type gelf_chunker: GELFWarningChunker
        """
        BaseGELFHandler.__init__(self, **kwargs)
        DatagramHandler.__init__(self, host, port)
        self.gelf_chunker = gelf_chunker

    def send(self, s):
        if len(s) < self.gelf_chunker.chunk_size:
            super(GELFUDPHandler, self).send(s)
        else:
            for chunk in self.gelf_chunker.chunk_message(s):
                super(GELFUDPHandler, self).send(chunk)
