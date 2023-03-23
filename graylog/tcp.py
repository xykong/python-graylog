from logging.handlers import SocketHandler

from graylog.handlers import BaseGELFHandler


class GELFTCPHandler(BaseGELFHandler, SocketHandler):
    """GELF TCP handler"""

    def __init__(self, host, port=12201, **kwargs):
        """Initialize the GELFTCPHandler

        :param host: GELF TCP input host.
        :type host: str

        :param port: GELF TCP input port.
        :type port: int

        .. attention::
            GELF TCP does not support compression due to the use of the null
            byte (``\\0``) as frame delimiter.

            Thus, :class:`.handler.GELFTCPHandler` does not support setting
            ``compress`` to :obj:`True` and is locked to :obj:`False`.
        """
        BaseGELFHandler.__init__(self, compress=False, **kwargs)
        SocketHandler.__init__(self, host, port)

    def makePickle(self, record):
        """Add a null terminator to generated pickles as TCP frame objects
        need to be null terminated

        :param record: :class:`logging.LogRecord` to create a null
            terminated GELF log.
        :type record: logging.LogRecord

        :return: Null terminated bytes representing a GELF log.
        :rtype: bytes
        """
        return super(GELFTCPHandler, self).makePickle(record) + b"\x00"
