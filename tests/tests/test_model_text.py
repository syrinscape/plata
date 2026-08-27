import unittest
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.checks import Tags, run_checks

from plata.contact.models import Contact
from plata.discount.models import Discount
from plata.shop.models import (
    Order,
    OrderItem,
    OrderPayment,
    OrderStatus,
    TaxClass,
)
from tests.models import Product


class ModelTextRepresentationTests(unittest.TestCase):
    def test_active_shop_models_have_caller_facing_text(self):
        user = User(username='Bjorn')
        contact = Contact(user=user, currency='CHF')
        discount = Discount(name='Launch sale')
        tax_class = TaxClass(name='GST')
        order = Order(_order_id='O-000000001')
        product = Product(name='Dragon cave')
        item = OrderItem(order=order, product=product, quantity=1)
        status = OrderStatus(order=order, status=Order.PAID)
        payment = OrderPayment(
            order=order,
            currency='CHF',
            amount=Decimal('1.00'),
            authorized=date.today(),
        )
        self.assertEqual(str(contact), 'Bjorn')
        self.assertEqual(str(discount), 'Launch sale')
        self.assertEqual(str(tax_class), 'GST')
        self.assertEqual(str(order), 'O-000000001')
        self.assertEqual(str(item), '1 of Dragon cave')
        self.assertEqual(
            str(status),
            'Status Order has been paid for O-000000001',
        )
        self.assertEqual(
            str(payment),
            'Authorized of CHF 1.00 for O-000000001',
        )

    def test_admin_configuration_accepts_active_text_columns(self):
        errors = run_checks(tags=[Tags.admin])

        self.assertEqual(errors, [])
