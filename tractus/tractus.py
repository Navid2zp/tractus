import json
import socket
import time
from typing import Union
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class TraceResult:
    __slots__ = 'status_code', 'dns', 'handshake', "first_byte", 'full_data', 'data_length', 'headers_length', 'ip'

    def __init__(self, status_code=0, dns=0.0, handshake=0.0, first_byte=0.0, full_data=0.0, data_length=0,
                 headers_length=0, ip=None):
        self.dns: float = dns
        self.handshake: float = handshake
        self.first_byte: float = first_byte
        self.full_data: float = full_data
        self.data_length: float = data_length
        self.headers_length: float = headers_length
        self.status_code: int = status_code
        self.ip: Union[str, None] = ip

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
        self.__stream = None
        self.__metrics: dict = {
            "dns": 0.0,
            "handshake": 0.0,
            "first_byte": 0.0,
            "full_data": 0.0,
            "data_length": 0,
            "headers_length": 0,
            "status_code": 0,
            "ip": None
        }

    def __get_dns_time(self):
        """
        Get IP address of the hostname.
        :return: float: time took in ms
        """
        try:
            dns_start = time.time()
            self.__metrics["ip"] = socket.gethostbyname(self.__hostname)
            return (time.time() - dns_start) * 1000
        except:
            return 0.0

    def __build_request(self):
        self.__request = Request(self.__url)

    def __open_url(self):
        """
        Open the url if dns was successful and measure handshake time and set the status code.
        """

        # Get the dns time first so we can subtract it from urlopen time to get handshake time
        self.__metrics["dns"] = self.__get_dns_time()

        # Return if ip is None which means we failed to resolve the host.
        if not self.__metrics["ip"]:
            return

        handshake_start = time.time()
        try:
            self.__stream = urlopen(self.__request)
            self.__metrics["status_code"] = self.__stream.code
        except HTTPError as e:  # errors such as 404, 500 and etc.
            self.__metrics["status_code"] = e.code
        except Exception:
            return
        # urlopen time includes dns lookup too
        # so subtract dns time to get handshake time
        self.__metrics["handshake"] = ((time.time() - handshake_start) * 1000) - self.__metrics["dns"]

    def __measure_data(self):
        # First byte
        first_b_s = time.time()
        self.__stream.read(1)
        self.__metrics["first_byte"] = (time.time() - first_b_s) * 1000

        # Full data
        data_start = time.time()
        self.__metrics["data_length"] = len(self.__stream.read())
        self.__metrics["full_data"] = (time.time() - data_start) * 1000

    def __get_metrics(self) -> dict:
        """
        Gather all the metrics.
        :return: dict: metrics for handshake, first byte and etc.
        """
        self.__open_url()

        # If request failed
        if self.__metrics["status_code"] == 0:
            return self.__metrics
        self.__measure_data()

        return self.__metrics

    def trace(self) -> TraceResult:
        self.__build_request()
        return TraceResult(
            **self.__get_metrics()
        )
