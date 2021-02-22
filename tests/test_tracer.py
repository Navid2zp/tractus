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
        self.assertTrue(hasattr(self.result, 'status_code'))
        self.assertTrue(hasattr(self.result, 'dns'))
        self.assertTrue(hasattr(self.result, 'handshake'))
        self.assertTrue(hasattr(self.result, 'redirects'))
        self.assertTrue(hasattr(self.result, 'first_byte'))
        self.assertTrue(hasattr(self.result, 'total'))
        self.assertTrue(hasattr(self.result, 'body_length'))
        self.assertTrue(hasattr(self.result, 'headers_length'))
        self.assertTrue(hasattr(self.result, 'ip'))

    def test_data_types(self):
        self.assertIsInstance(getattr(self.result, 'status_code'), int)
        self.assertIsInstance(getattr(self.result, 'dns'), int)
        self.assertIsInstance(getattr(self.result, 'handshake'), int)
        self.assertIsInstance(getattr(self.result, 'redirects'), int)
        self.assertIsInstance(getattr(self.result, 'first_byte'), int)
        self.assertIsInstance(getattr(self.result, 'total'), int)
        self.assertIsInstance(getattr(self.result, 'body_length'), int)
        self.assertIsInstance(getattr(self.result, 'headers_length'), int)

        self.assertTrue(type(getattr(self.result, 'ip')) == str)

    def test_data_values(self):
        self.assertEqual(getattr(self.result, 'status_code'), 200)
        # DNS might get cached
        self.assertTrue(getattr(self.result, 'dns') >= 0)
        self.assertTrue(getattr(self.result, 'total') >= 0)
        self.assertTrue(getattr(self.result, 'handshake') > 0)
        # Full data can be downloaded in less than a ms
        self.assertTrue(getattr(self.result, 'connect') >= 0)
        self.assertTrue(getattr(self.result, 'headers_length') > 0)
        self.assertTrue(getattr(self.result, 'body_length') > 0)
