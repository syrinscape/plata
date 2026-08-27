import unittest

from plata.shop.models import Order, OrderItem
from tests.models import Product


class ProductSnapshotTests(unittest.TestCase):
    def test_order_item_retains_unicode_product_name(self):
        product = Product(name='Bj\u00f6rk')
        order_item = OrderItem(order=Order(), product=product, quantity=1)

        product.handle_order_item(order_item)

        self.assertIsInstance(order_item.name, str)
        self.assertEqual(order_item.name, 'Bj\u00f6rk')
