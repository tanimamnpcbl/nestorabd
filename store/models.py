from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to='products/'
    )

    author = models.CharField(
        max_length=255,
        blank=True
    )

    brand = models.CharField(
        max_length=255,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    @property
    def current_price(self):

        if self.sale_price:
            return self.sale_price

        return self.price


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
        ('upay', 'Upay'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    order_number = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=30
    )

    email = models.EmailField()

    country = models.CharField(
        max_length=100,
        default='Bangladesh'
    )

    district = models.CharField(
        max_length=100
    )

    thana = models.CharField(
        max_length=100
    )

    address = models.TextField()

    order_note = models.TextField(
        blank=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_number = models.CharField(
        max_length=50,
        blank=True
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    payment_screenshot = models.ImageField(
        upload_to='payments/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    product_name = models.CharField(
        max_length=255
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):

        return f'{self.product_name} × {self.quantity}'