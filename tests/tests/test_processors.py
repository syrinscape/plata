import unittest
from decimal import Decimal

import plata
from plata.shop.processors import FixedAmountShippingProcessor, TaxProcessor


class Order(object):
    def __init__(self):
        self.data = {}


class Item(object):
    _line_item_price = Decimal('10.00')
    _line_item_discount = Decimal('0.00')
    tax_rate = Decimal('10.0')


class TaxProcessorTests(unittest.TestCase):
    def test_tax_details_are_stored_as_reusable_pairs(self):
        order = Order()

        TaxProcessor({}).process(order, [Item()])

        expected = [
            (
                Decimal('10.0'),
                {
                    'prices': Decimal('10.00'),
                    'discounts': Decimal('0.00'),
                    'tax_rate': Decimal('10.0'),
                    'tax_amount': Decimal('1.0000000000'),
                    'total': Decimal('11.0000000000'),
                },
            ),
        ]
        self.assertEqual(order.data['tax_details'], expected)
        self.assertEqual(list(order.data['tax_details']), expected)

    def test_shipping_tax_details_remain_reusable(self):
        previous = plata.settings.PLATA_SHIPPING_FIXEDAMOUNT
        self.addCleanup(
            setattr,
            plata.settings,
            'PLATA_SHIPPING_FIXEDAMOUNT',
            previous,
        )
        plata.settings.PLATA_SHIPPING_FIXEDAMOUNT = {
            'cost': Decimal('11.00'),
            'tax': Decimal('10.0'),
        }
        order = Order()
        order.discount_remaining = Decimal('0.00')

        FixedAmountShippingProcessor({}).process(order, [])

        expected = [
            (
                Decimal('10.0'),
                {
                    'prices': Decimal('10.00'),
                    'discounts': Decimal('0.00'),
                    'tax_rate': Decimal('10.0'),
                    'tax_amount': Decimal('1.00'),
                    'total': Decimal('11.00'),
                },
            ),
        ]
        self.assertEqual(order.data['tax_details'], expected)
        self.assertEqual(list(order.data['tax_details']), expected)
