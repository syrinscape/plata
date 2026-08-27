import unittest

from plata.fields import json_encode_default


class UnsupportedValue(object):
    def __repr__(self):
        return 'unsupported'


class JSONEncodeDefaultTests(unittest.TestCase):
    def test_unsupported_value_raises_type_error(self):
        with self.assertRaises(TypeError) as error:
            json_encode_default(UnsupportedValue())

        self.assertEqual(error.exception.args, ('Cannot encode unsupported',))
