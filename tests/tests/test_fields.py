import unittest

from plata.fields import CurrencyField, JSONField, json_encode_default


class CurrencyFieldChoicesTests(unittest.TestCase):
    def test_currency_choices_are_reusable(self):
        expected = [
            ('CHF', 'CHF'),
            ('EUR', 'EUR'),
            ('USD', 'USD'),
            ('CAD', 'CAD'),
        ]

        self.assertEqual(list(CurrencyField().choices), expected)
        self.assertEqual(list(CurrencyField().choices), expected)


class JSONFieldConversionTests(unittest.TestCase):
    def test_text_values_are_decoded_and_mappings_are_encoded(self):
        field = JSONField()

        self.assertEqual(field.to_python('{"count": 2}'), {'count': 2})
        self.assertEqual(field.get_prep_value({'count': 2}), '{"count": 2}')


class UnsupportedValue(object):
    def __repr__(self):
        return 'unsupported'


class JSONEncodeDefaultTests(unittest.TestCase):
    def test_unsupported_value_raises_type_error(self):
        with self.assertRaises(TypeError) as error:
            json_encode_default(UnsupportedValue())

        self.assertEqual(error.exception.args, ('Cannot encode unsupported',))
