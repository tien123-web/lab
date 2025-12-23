from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('search/', views.search, name="search"),
    path('detail/', views.detail, name="detail"),
    path('category/', views.category, name="category"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('sale/', views.sale_page, name='sale'),
    # Product detail review
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('process_order/', views.processOrder, name='process_order'),

    # THÊM CÁC URL SAU ĐÂY - Thanh toán và đơn hàng mới
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('order/history/', views.order_history, name='order_history'),
    path('order/detail/<int:order_id>/', views.order_detail, name='order_detail'),

    # URL DUY NHẤT cho tất cả phương thức thanh toán
    path('payment/<int:order_id>/<str:payment_method>/', views.payment_gateway, name='payment_gateway'),

    # Callback URLs - THÊM DÒNG NÀY
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/momo-callback/', views.momo_callback, name='momo_callback'),
]