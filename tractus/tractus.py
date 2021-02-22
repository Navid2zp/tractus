import json
from typing import Union
from urllib.request import Request

import pycurl


class Storage:
    def __init__(self):
        self.contents = b''

    def store(self, buf: bytes):
        self.contents += buf

    def get_length(self):
        return len(self.contents)

    def __str__(self):
        return str(self.contents)


class TraceResult:
    __slots__ = 'status_code', 'dns', 'handshake', 'connect', "first_byte", 'total', 'body_length', 'headers_length', \
                'ip', 'redirects'

    def __init__(self, status_code=0, dns=0, handshake=0, first_byte=0, total=0, body_length=0, redirects=0, connect=0,
                 headers_length=0, ip=None):
        self.dns: int = dns
        self.redirects: int = redirects
        self.handshake: int = handshake
        self.first_byte: int = first_byte
        self.total: int = total
        self.connect: int = connect
        self.body_length: int = body_length
        self.headers_length: int = headers_length
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

    def __init__(self, url: str, method: str = "GET", headers=None, data=None):
        self.__url = url
        self.__headers = {} if not headers else headers
        self.__data = data if (type(data) == bytes or data is None) else data.encode()
        self.__method = method.upper()
        # Extract hostname
        self.__curl: pycurl.Curl
        self.__headers_storage: Storage = Storage()
        self.__body_storage: Storage = Storage()
        self.__metrics: dict = {
            "dns": 0,
            "handshake": 0,
            "redirects": 0,
            "connect": 0,
            "first_byte": 0,
            "total": 0,
            "body_length": 0,
            "headers_length": 0,
            "status_code": 0,
            "ip": None
        }

    def __set_headers(self):
        if self.__headers and len(self.__headers) > 0:
            headers = []
            for key in self.__headers.keys():
                headers.append(f'{key}: {self.__headers[key]}')
            self.__curl.setopt(pycurl.HTTPHEADER, headers)

    def __set_data(self):
        if self.__data:
            self.__curl.setopt(pycurl.POSTFIELDS, self.__data)

    def __build_request(self):
        self.__request = Request(self.__url, headers=self.__headers, method=self.__method)
        self.__curl = pycurl.Curl()
        self.__curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        self.__curl.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        self.__curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.__curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.__curl.setopt(pycurl.DNS_CACHE_TIMEOUT, 0)
        self.__curl.setopt(pycurl.URL, self.__url)
        self.__curl.setopt(pycurl.CUSTOMREQUEST, self.__method)
        self.__curl.setopt(self.__curl.HEADERFUNCTION, self.__headers_storage.store)
        self.__curl.setopt(self.__curl.WRITEFUNCTION, self.__body_storage.store)
        self.__set_headers()
        self.__set_data()

    def __gather_info(self):
        self.__metrics["dns"] = round(self.__curl.getinfo(pycurl.NAMELOOKUP_TIME) * 1000)
        self.__metrics["redirects"] = round(self.__curl.getinfo(pycurl.REDIRECT_TIME) * 1000)
        self.__metrics["handshake"] = round(self.__curl.getinfo(pycurl.APPCONNECT_TIME) * 1000)
        self.__metrics["connect"] = round(self.__curl.getinfo(pycurl.CONNECT_TIME) * 1000)
        self.__metrics["first_byte"] = round(self.__curl.getinfo(pycurl.STARTTRANSFER_TIME) * 1000)
        self.__metrics["total"] = round(self.__curl.getinfo(pycurl.TOTAL_TIME) * 1000)
        self.__metrics["status_code"] = self.__curl.getinfo(pycurl.HTTP_CODE)
        self.__metrics["ip"] = self.__curl.getinfo(pycurl.PRIMARY_IP)
        self.__metrics["headers_length"] = self.__headers_storage.get_length()
        self.__metrics["body_length"] = self.__body_storage.get_length()

    def __measure(self):
        self.__curl.perform()
        self.__gather_info()
        self.__curl.close()
        return self.__metrics

    def trace(self) -> TraceResult:
        self.__build_request()
        return TraceResult(
            **self.__measure()
        )
