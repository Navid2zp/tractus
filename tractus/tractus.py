import json
import socket
import time
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class TraceResult:
    __slots__ = 'dns', 'handshake', "first_byte", 'full_data', 'data_length'

    def __init__(self, dns, handshake, first_byte, full_data, data_length):
        self.dns: float = dns
        self.handshake: float = handshake
        self.first_byte: float = first_byte
        self.full_data: float = full_data
        self.data_length: float = data_length

    @property
    def __dict__(self):
        """
        Convert data to dict
        :return: dict: results as dict
        """
        return {s: getattr(self, s) for s in self.__slots__ if hasattr(self, s)}

    def as_dict(self) -> dict:
        return self.__dict__

    def as_json(self) -> str:
        """
        Converts results to json
        :return: str: json converted results
        """
        return json.dumps(self.__dict__)


class Tracer:
    """
    Main tracer class.
    Gathers all the metrics and returns the results.
    """

    def __init__(self, url: str):
        self.__url = url
        # Extract hostname
        self.__hostname = urlparse(url).hostname
        self.__request: Request

    def __get_dns_time(self):
        """
        Get IP address of the hostname.
        :return: float: time took in ms
        """

        dns_start = time.time()
        socket.gethostbyname(self.__hostname)
        return (time.time() - dns_start) * 1000

    def __build_request(self):
        self.__request = Request(self.__url)

    def __get_metrics(self, dns_time: float) -> dict:
        """
        Gather all the metrics.
        :param dns_time: float - time took for dns lookup to be subtracted from handshake.
        :return: dict: metrics for handshake, first byte and etc.
        """
        handshake_start = time.time()
        stream = urlopen(self.__request)
        # urlopen time includes dns lookup too
        # so get the dns time and subtract it from handshake time
        handshake = ((time.time() - handshake_start) * 1000) - dns_time

        # First byte
        first_b_s = time.time()
        stream.read(1)
        first_byte = (time.time() - first_b_s) * 1000

        # Full data
        data_start = time.time()
        full_data_length = len(stream.read())
        full_data = (time.time() - data_start) * 1000

        return {
            "handshake": handshake,
            "first_byte": first_byte,
            "full_data": full_data,
            "data_length": full_data_length
        }

    def trace(self) -> TraceResult:
        dns = self.__get_dns_time()
        self.__build_request()

        return TraceResult(
            dns=dns,
            **self.__get_metrics(dns)
        )
