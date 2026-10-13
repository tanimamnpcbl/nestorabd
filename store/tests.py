from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CartQuantityTests(TestCase):

    def setUp(self):
        category = Category.objects.create(
            name='Books',
            slug='books'
        )
        self.product = Product.objects.create(
            category=category,
            name='Test Book',
            slug='test-book',
            sku='TEST-001',
            description='Test product',
            price='100.00',
            stock=5,
            image='products/test.jpg'
        )
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

    def test_update_cart_quantity(self):
        response = self.client.post(
            reverse('cart_update', args=[self.product.id]),
            {'quantity': 3}
        )

        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(
            self.client.session['cart'][str(self.product.id)],
            3
        )

    def test_quantity_cannot_exceed_stock(self):
        self.client.post(
            reverse('cart_update', args=[self.product.id]),
            {'quantity': 6}
        )

        self.assertEqual(
            self.client.session['cart'][str(self.product.id)],
            1
        )

    def test_increment_and_decrement_quantity(self):
        url = reverse('cart_update', args=[self.product.id])

        self.client.post(url, {'action': 'increment'})
        self.assertEqual(
            self.client.session['cart'][str(self.product.id)],
            2
        )

        self.client.post(url, {'action': 'decrement'})
        self.assertEqual(
            self.client.session['cart'][str(self.product.id)],
            1
        )

    def test_zero_quantity_removes_item(self):
        self.client.post(
            reverse('cart_update', args=[self.product.id]),
            {'quantity': 0}
        )

        self.assertNotIn(
            str(self.product.id),
            self.client.session['cart']
        )
