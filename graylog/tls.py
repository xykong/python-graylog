import socket
import ssl

from graylog import GELFTCPHandler


class GELFTLSHandler(GELFTCPHandler):
    """GELF TCP handler with TLS support"""

    def __init__(
            self,
            host,
            port=12204,
            validate=False,
            ca_certs=None,
            certfile=None,
            keyfile=None,
            **kwargs
    ):
        """Initialize the GELFTLSHandler

        :param host: GELF TLS input host.
        :type host: str

        :param port: GELF TLS input port.
        :type port: int

        :param validate: If :obj:`True`, validate the Graylog server's
            certificate. In this case specifying ``ca_certs`` is also
            required.
        :type validate: bool

        :param ca_certs: Path to CA bundle file.
        :type ca_certs: str

        :param certfile: Path to the client certificate file.
        :type certfile: str

        :param keyfile: Path to the client private key. If the private key is
            stored with the certificate, this parameter can be ignored.
        :type keyfile: str
        """
        if validate and ca_certs is None:
            raise ValueError("CA bundle file path must be specified")

        if keyfile is not None and certfile is None:
            raise ValueError("certfile must be specified")

        GELFTCPHandler.__init__(self, host=host, port=port, **kwargs)

        self.ca_certs = ca_certs
        self.reqs = ssl.CERT_REQUIRED if validate else ssl.CERT_NONE
        self.certfile = certfile
        self.keyfile = keyfile if keyfile else certfile

    def makeSocket(self, timeout=1):
        """Create a TLS wrapped socket"""
        plain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if hasattr(plain_socket, "settimeout"):
            plain_socket.settimeout(timeout)

        wrapped_socket = ssl.wrap_socket(
            plain_socket,
            ca_certs=self.ca_certs,
            cert_reqs=self.reqs,
            keyfile=self.keyfile,
            certfile=self.certfile,
        )
        wrapped_socket.connect((self.host, self.port))

        return wrapped_socket
