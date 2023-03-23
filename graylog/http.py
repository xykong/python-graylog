from http import client as httplib

from graylog.handlers import BaseGELFHandler


class GELFHTTPHandler(BaseGELFHandler):
    """GELF HTTP handler"""

    def __init__(
            self, host, port=12203, compress=True, path="/gelf", timeout=5, **kwargs
    ):
        """Initialize the GELFHTTPHandler

        :param host: GELF HTTP input host.
        :type host: str

        :param port: GELF HTTP input port.
        :type port: int

        :param compress: If :obj:`True` compress the GELF message before
            sending it to the Graylog server.
        :type compress: bool

        :param path: Path of the HTTP input.
            (see https://docs.graylog.org/en/latest/pages/sending_data.html#gelf-via-http)
        :type path: str

        :param timeout: Number of seconds the HTTP client should wait before
            it discards the request if the Graylog server doesn't respond.
        :type timeout: int
        """
        BaseGELFHandler.__init__(self, compress=compress, **kwargs)

        self.host = host
        self.port = port
        self.path = path
        self.timeout = timeout
        self.headers = {}

        if compress:
            self.headers["Content-Encoding"] = "gzip,deflate"

    def emit(self, record):
        """Convert a :class:`logging.LogRecord` to GELF and emit it to Graylog
        via an HTTP POST request

        :param record: :class:`logging.LogRecord` to convert into a GELF log
            and emit to Graylog via an HTTP POST request.
        :type record: logging.LogRecord
        """
        pickle = self.makePickle(record)
        connection = httplib.HTTPConnection(
            host=self.host, port=self.port, timeout=self.timeout
        )
        connection.request("POST", self.path, pickle, self.headers)
