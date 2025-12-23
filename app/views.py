from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
import json
import datetime
import hashlib
import hmac
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def detail(request):
    # dang nhap moi duoc mua hang
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    reviews = []
    if products.exists():
        reviews = Review.objects.filter(product=products.first())
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               'products': products, 'categories': categories, 'reviews': reviews}
    return render(request, 'app/detail.html', context)

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Kiểm tra rating hợp lệ
        if not rating or not comment:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin')
        else:
            # Tạo review
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Đã thêm đánh giá!')

    # Redirect về trang chi tiết sản phẩm
    return redirect('/detail/?id=' + str(product_id))

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Chỉ cho phép xóa review của chính mình
    if review.user != request.user:
        messages.error(request, 'Không có quyền xóa')
        return redirect('home')

    product_id = review.product.id
    review.delete()
    messages.success(request, 'Đã xóa đánh giá')

    # Redirect về trang chi tiết sản phẩm
    return redirect('/detail/?id=' + str(product_id))

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {'categories': categories, 'active_category': active_category, 'products': products}
    return render(request, 'app/category.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request, 'app/search.html',
                  {'searched': searched, 'keys': keys, 'products': products, 'cartItems': cartItems})

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    categories = Category.objects.filter(is_sub=False)
    context = {'form': form, 'categories': categories}
    return render(request, 'app/register.html', context)

# trung ten voi django
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Tên đăng nhập hoặc mật khẩu chưa chính xác')
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories}
    return render(request, 'app/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # hien thi so san pham tren gio hang
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'categories': categories}
    return render(request, 'app/home.html', context)

def cart(request):
    # dang nhap moi duoc mua hang
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    categories = Category.objects.filter(is_sub=False)
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'categories': categories}
    return render(request, 'app/cart.html', context)

# =========== CÁC HÀM HELPER CHO THANH TOÁN (PHẢI ĐẶT TRƯỚC checkout) ===========

def generate_transaction_id():
    """Tạo mã giao dịch duy nhất"""
    import uuid
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = uuid.uuid4().hex[:6].upper()
    return f'ORD{timestamp}{random_str}'

def handle_cod_payment(request, order, payment):
    """Xử lý thanh toán khi nhận hàng"""
    payment.status = 'completed'
    payment.paid_at = datetime.datetime.now()
    payment.save()

    order.complete = True
    order.payment_status = 'completed'
    order.save()

    messages.success(
        request,
        f'Đặt hàng thành công! Mã đơn hàng: {order.id}. '
        f'Bạn sẽ thanh toán {payment.amount:,.0f}₫ khi nhận hàng.'
    )

    return redirect('order_success', order_id=order.id)

def handle_bank_transfer(request, order, payment):
    """Xử lý chuyển khoản ngân hàng"""
    bank_info = {
        'bank_name': 'Vietcombank',
        'account_number': '1234567890',
        'account_holder': 'CÔNG TY TNHH THỰC PHẨM ABC',
        'branch': 'Chi nhánh Hà Nội',
        'amount': f'{payment.amount:,.0f}₫',
        'content': f'THANHTOAN {order.transaction_id}'
    }

    # Lưu thông tin vào session để hiển thị ở trang tiếp theo
    request.session['bank_info'] = bank_info
    request.session['order_id'] = order.id

    return redirect('bank_transfer_info')

def handle_momo_payment(request, order, payment):
    """Xử lý thanh toán qua MoMo"""
    try:
        # Tạo yêu cầu thanh toán MoMo
        momo_transaction_id = f'MOMO_{uuid.uuid4().hex[:10]}'
        payment.transaction_id = momo_transaction_id
        payment.save()

        # Giả lập redirect đến MoMo
        request.session['momo_order_id'] = order.id
        request.session['momo_amount'] = payment.amount

        # Chuyển đến trang giả lập thanh toán MoMo
        return redirect('momo_payment', order_id=order.id)

    except Exception as e:
        messages.error(request, f'Lỗi khi tạo yêu cầu thanh toán MoMo: {str(e)}')
        return redirect('checkout')

# =========== HÀM CHECKOUT ===========

def checkout(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Vui lòng đăng nhập để thanh toán')
        return redirect('login')

    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    # KIỂM TRA GIỎ HÀNG TRỐNG - CHUYỂN HƯỚNG NGAY
    if not items:
        messages.error(request, 'Giỏ hàng của bạn đang trống')
        return redirect('cart')
    cartItems = order.get_cart_items

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        district = request.POST.get('district')
        ward = request.POST.get('ward')
        payment_method = request.POST.get('payment_method')

        # Kiểm tra thông tin bắt buộc
        required_fields = ['full_name', 'phone', 'address', 'city', 'district', 'ward']
        for field in required_fields:
            if not request.POST.get(field):
                messages.error(request, f'Vui lòng nhập đầy đủ thông tin {field.replace("_", " ")}')
                return redirect('checkout')

        # Cập nhật thông tin đơn hàng
        order.full_name = full_name
        order.phone = phone
        order.address = address
        order.city = city
        order.district = district
        order.ward = ward
        order.payment_method = payment_method
        order.transaction_id = generate_transaction_id()

        order.save()

        # Tạo bản ghi thanh toán
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.final_total,
            transaction_id=order.transaction_id
        )
        # Đánh dấu đơn hàng đã hoàn thành
        order.complete = True
        order.payment_status = 'completed'
        order.save()

        # Xử lý thanh toán theo phương thức
        if payment_method == 'COD':
            messages.success(request,
                             f'Đặt hàng thành công! Mã đơn hàng: {order.transaction_id}. Bạn sẽ thanh toán khi nhận hàng.')
            return redirect('order_success', order_id=order.id)
        elif payment_method == 'BANK':
            # Chuyển đến payment_gateway với phương thức BANK
            return redirect('payment_gateway', order_id=order.id, payment_method='BANK')
        elif payment_method == 'MOMO':
            # Chuyển đến payment_gateway với phương thức MOMO
            return redirect('payment_gateway', order_id=order.id, payment_method='MOMO')
        elif payment_method == 'ZALO':
            # Chuyển đến payment_gateway với phương thức ZALO
            return redirect('payment_gateway', order_id=order.id, payment_method='ZALO')
        elif payment_method == 'VISA':
            # Chuyển đến payment_gateway với phương thức VISA
            return redirect('payment_gateway', order_id=order.id, payment_method='VISA')
        else:
            messages.error(request, 'Phương thức thanh toán không được hỗ trợ')
            return redirect('checkout')

    categories = Category.objects.filter(is_sub=False)

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'categories': categories,
        'payment_methods': Payment.PAYMENT_METHODS
    }
    return render(request, 'app/checkout.html', context)

# =========== CÁC HÀM SAU THANH TOÁN ===========

def order_success(request, order_id):
    """Trang hiển thị sau khi đặt hàng thành công"""
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, customer=request.user)
    payment = Payment.objects.filter(order=order).first()

    # Xóa session nếu có
    if 'bank_info' in request.session:
        del request.session['bank_info']
    if 'momo_order_id' in request.session:
        del request.session['momo_order_id']

    categories = Category.objects.filter(is_sub=False)

    context = {
        'order': order,
        'payment': payment,
        'categories': categories,
        'cartItems': 0  # Giỏ hàng đã trống
    }
    return render(request, 'app/order_success.html', context)

def bank_transfer_info(request):
    """Hiển thị thông tin chuyển khoản ngân hàng"""
    bank_info = request.session.get('bank_info', {})
    order_id = request.session.get('order_id')

    if not bank_info or not order_id:
        return redirect('checkout')

    order = get_object_or_404(Order, id=order_id, customer=request.user)

    categories = Category.objects.filter(is_sub=False)

    context = {
        'bank_info': bank_info,
        'order': order,
        'categories': categories,
        'cartItems': 0
    }
    return render(request, 'app/bank_transfer_info.html', context)

def momo_payment(request, order_id):
    """Trang thanh toán MoMo (giả lập)"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    payment = Payment.objects.filter(order=order).first()

    categories = Category.objects.filter(is_sub=False)

    context = {
        'order': order,
        'payment': payment,
        'categories': categories,
        'cartItems': 0
    }
    return render(request, 'app/momo_payment.html', context)

@csrf_exempt
def momo_callback(request):
    """Callback từ MoMo (giả lập)"""
    if request.method == 'POST':
        # Trong thực tế, bạn sẽ nhận data từ MoMo
        order_id = request.POST.get('orderId')
        result_code = request.POST.get('resultCode', '0')

        if result_code == '0':  # Thanh toán thành công
            order = get_object_or_404(Order, id=order_id)
            payment = Payment.objects.filter(order=order).first()

            if payment:
                payment.status = 'completed'
                payment.paid_at = datetime.datetime.now()
                payment.save()

                order.complete = True
                order.payment_status = 'completed'
                order.save()

            return JsonResponse({'status': 'success', 'message': 'Thanh toán thành công'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Thanh toán thất bại'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def processOrder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer = request.user

        try:
            order = Order.objects.get(customer=customer, complete=False)

            # Cập nhật thông tin đơn hàng
            order.full_name = data['name']
            order.phone = data['phone']
            order.address = f"{data['address']}, {data['ward']}, {data['district']}, {data['city']}"
            order.city = data['city']
            order.district = data['district']
            order.ward = data['ward']

            # Tạo mã giao dịch
            order.transaction_id = generate_transaction_id()

            # Lưu đơn hàng (chưa complete)
            order.save()

            # Tạo bản ghi thanh toán
            payment = Payment.objects.create(
                order=order,
                payment_method='COD',  # Mặc định COD
                amount=order.final_total,
                transaction_id=order.transaction_id,
                status='pending'
            )

            return JsonResponse({
                'status': 'success',
                'order_id': order.id,
                'transaction_id': order.transaction_id
            }, safe=False)

        except Order.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Không tìm thấy đơn hàng'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def order_history(request):
    """Lịch sử đơn hàng của khách hàng"""
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(customer=request.user, complete=True).order_by('-date_ordered')
    categories = Category.objects.filter(is_sub=False)

    context = {
        'orders': orders,
        'categories': categories,
        'cartItems': 0
    }
    return render(request, 'app/order_history.html', context)

def order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.orderitem_set.all()
    payment = Payment.objects.filter(order=order).first()

    categories = Category.objects.filter(is_sub=False)

    context = {
        'order': order,
        'items': items,
        'payment': payment,
        'categories': categories,
        'cartItems': 0
    }
    return render(request, 'app/order_detail.html', context)

# them san pham vao gio hang
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)

def sale_page(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0
    categories = Category.objects.filter(is_sub=False)
    SALE_PRICE_LIMIT = 30000
    sale_products = Product.objects.filter(price__lt=SALE_PRICE_LIMIT)
    sort = request.GET.get('sort')
    product_type = request.GET.get('type')
    if product_type == 'drink':
        sale_products = sale_products.filter(drink=True)
    elif product_type == 'cake':
        sale_products = sale_products.filter(drink=False)
    if sort == 'price_asc':
        sale_products = sale_products.order_by('price')
    elif sort == 'price_desc':
        sale_products = sale_products.order_by('-price')
    context = {
        'sale_products': sale_products,
        'cartItems': cartItems,
        'categories': categories
    }
    return render(request, 'app/sale.html', context)


def payment_gateway(request, order_id, payment_method):
    """Xử lý tất cả các phương thức thanh toán trong một view"""
    if not request.user.is_authenticated:
        return redirect('login')

    order = get_object_or_404(Order, id=order_id, customer=request.user)
    payment = Payment.objects.filter(order=order).first()

    # Thông tin thanh toán cho từng phương thức
    payment_info = {
        'BANK': {
            'title': 'Chuyển khoản ngân hàng',
            'banks': [
                {
                    'name': 'Vietcombank',
                    'account_number': '1234567890',
                    'account_holder': 'CÔNG TY TNHH CAFE & BANH',
                    'branch': 'Chi nhánh Hà Nội'
                },
                {
                    'name': 'Techcombank',
                    'account_number': '0987654321',
                    'account_holder': 'CÔNG TY TNHH CAFE & BANH',
                    'branch': 'Chi nhánh TP.HCM'
                },
                {
                    'name': 'BIDV',
                    'account_number': '1357924680',
                    'account_holder': 'CÔNG TY TNHH CAFE & BANH',
                    'branch': 'Chi nhánh Đà Nẵng'
                }
            ],
            'instructions': [
                'Đăng nhập vào Internet Banking/ Mobile Banking',
                'Chọn chức năng "Chuyển khoản"',
                'Nhập thông tin ngân hàng như bên trên',
                'Nhập số tiền chính xác: ' + f"{order.final_total:,.0f}₫",
                'Nhập nội dung chính xác: ' + order.transaction_id,
                'Xác nhận và hoàn tất giao dịch'
            ]
        },
        'MOMO': {
            'title': 'Ví MoMo',
            'phone': '0912345678',
            'account_name': 'NGUYEN VAN A',
            'content_prefix': 'MOMO_',
            'instructions': [
                'Mở ứng dụng MoMo trên điện thoại',
                'Chọn "Quét mã"',
                'Quét mã QR bên trên',
                'Kiểm tra thông tin và xác nhận thanh toán',
                'Chờ kết quả xác nhận'
            ]
        },
        'ZALO': {
            'title': 'ZaloPay',
            'payment_link': f'https://zalopay.vn/pay?order={order.transaction_id}&amount={order.final_total}',
            'instructions': [
                'Mở ứng dụng ZaloPay trên điện thoại',
                'Chọn "Quét mã" hoặc "Thanh toán bằng link"',
                'Quét mã QR hoặc mở link thanh toán',
                'Xác nhận thông tin và hoàn tất',
                'Chờ xác nhận từ hệ thống'
            ]
        },
        'VISA': {
            'title': 'Thẻ quốc tế',
            'instructions': [
                'Nhập đầy đủ thông tin thẻ bên dưới',
                'Kiểm tra kỹ thông tin trước khi xác nhận',
                'Xác thực 3D Secure (nếu được yêu cầu)',
                'Chờ xác nhận từ ngân hàng',
                'Giữ hóa đơn để đối chiếu nếu cần'
            ]
        }
    }

    # Kiểm tra phương thức thanh toán hợp lệ
    if payment_method not in payment_info:
        messages.error(request, 'Phương thức thanh toán không hợp lệ')
        return redirect('checkout')

    context = {
        'order': order,
        'payment': payment,
        'payment_method': payment_method,
        'payment_info': payment_info[payment_method],
        'categories': Category.objects.filter(is_sub=False),
        'cartItems': 0
    }

    return render(request, 'app/payment_gateway.html', context)


@csrf_exempt
def payment_callback(request):
    """Callback chung cho tất cả phương thức thanh toán"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status', 'success')

        order = get_object_or_404(Order, id=order_id)
        payment = Payment.objects.filter(order=order).first()

        if status == 'success':
            payment.status = 'completed'
            payment.paid_at = datetime.datetime.now()
            payment.save()

            order.complete = True
            order.payment_status = 'completed'
            order.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Thanh toán thành công',
                'order_id': order.id
            })
        else:
            payment.status = 'failed'
            payment.save()

            return JsonResponse({
                'status': 'error',
                'message': 'Thanh toán thất bại'
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})