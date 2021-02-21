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
        self.assertTrue(hasattr(self.result, 'first_byte'))
        self.assertTrue(hasattr(self.result, 'full_data'))
        self.assertTrue(hasattr(self.result, 'data_length'))
        self.assertTrue(hasattr(self.result, 'headers_length'))
        self.assertTrue(hasattr(self.result, 'ip'))

    def test_data_types(self):
        self.assertIsInstance(getattr(self.result, 'status_code'), int)
        self.assertIsInstance(getattr(self.result, 'dns'), int)
        self.assertIsInstance(getattr(self.result, 'handshake'), int)
        self.assertIsInstance(getattr(self.result, 'first_byte'), int)
        self.assertIsInstance(getattr(self.result, 'full_data'), int)
        self.assertIsInstance(getattr(self.result, 'data_length'), int)
        self.assertIsInstance(getattr(self.result, 'headers_length'), int)

        self.assertTrue(type(getattr(self.result, 'ip')) == str)

    def test_data_values(self):
        self.assertEqual(getattr(self.result, 'status_code'), 200)
        self.assertTrue(getattr(self.result, 'dns') > 0.0)
        self.assertTrue(getattr(self.result, 'handshake') > 0.0)
        self.assertTrue(getattr(self.result, 'full_data') > 0.0)
        self.assertTrue(getattr(self.result, 'headers_length') > 0.0)
        self.assertTrue(getattr(self.result, 'data_length') > 0.0)


class TestTracerBadURL(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Do a trace here to avoid duplicating request for each test case
        """
        cls.result = Tracer('https://bad.domain.huh').trace()

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
        self.assertTrue(hasattr(self.result, 'first_byte'))
        self.assertTrue(hasattr(self.result, 'full_data'))
        self.assertTrue(hasattr(self.result, 'data_length'))
        self.assertTrue(hasattr(self.result, 'headers_length'))
        self.assertTrue(hasattr(self.result, 'ip'))

    def test_data_types(self):
        self.assertIsInstance(getattr(self.result, 'status_code'), int)
        self.assertIsInstance(getattr(self.result, 'dns'), int)
        self.assertIsInstance(getattr(self.result, 'handshake'), int)
        self.assertIsInstance(getattr(self.result, 'first_byte'), int)
        self.assertIsInstance(getattr(self.result, 'full_data'), int)
        self.assertIsInstance(getattr(self.result, 'data_length'), int)
        self.assertIsInstance(getattr(self.result, 'headers_length'), int)

        self.assertTrue(not getattr(self.result, 'ip'))

    def test_data_values(self):
        self.assertEqual(getattr(self.result, 'status_code'), 0)
        self.assertEqual(getattr(self.result, 'dns'), 0)
        self.assertEqual(getattr(self.result, 'handshake'), 0)
        self.assertEqual(getattr(self.result, 'first_byte'), 0)
        self.assertEqual(getattr(self.result, 'full_data'), 0)
        self.assertEqual(getattr(self.result, 'data_length'), 0)
        self.assertEqual(getattr(self.result, 'headers_length'), 0)
        self.assertEqual(getattr(self.result, 'ip'), None)
