import json
import unittest

from tractus import Tracer, TraceResult


class TestTracer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Do a trace here to avoid duplicating request for each test case
        """
        cls.result = Tracer('https://google.com').trace()

    def test_result_type(self):
        self.assertIsInstance(self.result, TraceResult)

    def test_as_dict(self):
        self.assertIsInstance(self.result.as_dict(), dict)
        self.assertIsInstance(self.result.__dict__, dict)

    def test_json(self):
        json_data = self.result.as_json()
        json.loads(json_data)

    def test_attars(self):
        self.assertTrue(hasattr(self.result, 'dns'))
        self.assertTrue(hasattr(self.result, 'handshake'))
        self.assertTrue(hasattr(self.result, 'first_byte'))
        self.assertTrue(hasattr(self.result, 'full_data'))
        self.assertTrue(hasattr(self.result, 'data_length'))
