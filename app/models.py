from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True,
                                     blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Thay doi form register cua django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    drink = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='product')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    # xu ly loi khong co hinh anh
    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"


# ĐỊNH NGHĨA PAYMENT TRƯỚC
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Thanh toán khi nhận hàng'),
        ('BANK', 'Chuyển khoản ngân hàng'),
        ('MOMO', 'Ví MoMo'),
        ('ZALO', 'Ví ZaloPay'),
        ('VISA', 'Thẻ Visa/Mastercard'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('completed', 'Đã thanh toán'),
        ('failed', 'Thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    ]

    # Sử dụng string 'Order' thay vì Order để tránh circular import
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='COD')
    amount = models.FloatField()
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.id} - {self.order.id} - {self.get_payment_method_display()}"


# ORDER PHẢI ĐƯỢC ĐỊNH NGHĨA TRƯỚC OrderItem và ShippingAddress
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    # Thông tin giao hàng
    full_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)

    # Thông tin thanh toán
    payment_method = models.CharField(max_length=20, choices=Payment.PAYMENT_METHODS, default='COD')
    payment_status = models.CharField(max_length=20, choices=Payment.STATUS_CHOICES, default='pending')

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def shipping_fee(self):
        # Tính phí vận chuyển (ví dụ: miễn phí cho đơn > 300k)
        if self.get_cart_total > 300000:
            return 0
        return 30000

    @property
    def final_total(self):
        return self.get_cart_total + self.shipping_fee


# OrderItem và ShippingAddress PHẢI ĐẶT SAU Order
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address