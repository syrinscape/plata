from django.test import TestCase
from django.test.client import RequestFactory

import plata
from plata.contact.models import Contact
from plata.discount.models import Discount
from plata.shop.models import Order, OrderItem
from plata.shop.views import Shop
from tests.models import Product


class FormsetShop(Shop):
    def render_cart(self, request, context):
        return context


class Django18ShopTests(TestCase):
    def setUp(self):
        self.registered_shop = plata.shop_instance_cache

    def tearDown(self):
        plata.register(self.registered_shop)

    def test_non_empty_cart_builds_order_item_formset(self):
        product = Product.objects.create(name='Django 1.8 product')
        order = Order.objects.create(currency='CHF')
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=1,
            currency='CHF',
            _unit_price=0,
            _unit_tax=0,
            tax_rate=0,
            is_sale=False,
            data={},
        )

        shop = FormsetShop(Contact, Order, Discount)
        context = shop.cart(RequestFactory().get('/cart/'), order)

        formset = context['orderitemformset']
        self.assertIs(formset.model, OrderItem)
        self.assertEqual(
            [form.instance for form in formset.forms],
            [order_item],
        )

    def test_payment_modules_for_request_are_reusable(self):
        shop = FormsetShop(Contact, Order, Discount)
        payment_modules = shop.get_payment_modules(
            RequestFactory().get('/confirmation/')
        )

        first_pass = [module.__module__ for module in payment_modules]
        self.assertTrue(first_pass)
        self.assertEqual(
            [module.__module__ for module in payment_modules],
            first_pass,
        )
