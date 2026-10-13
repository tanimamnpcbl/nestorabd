from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.db.models import Prefetch, Q
from django.db import transaction

from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.utils import timezone

import uuid

from .models import (
    Product,
    Category,
    Order,
    OrderItem
)

from .forms import RegistrationForm


# =========================================================
# HOME PAGE
# =========================================================

def home(request):
    categories = Category.objects.filter(
        is_active=True
    ).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(
                is_active=True
            ).order_by('-created_at'),
            to_attr='active_products'
        )
    ).order_by('name')

    return render(
        request,
        'home.html',
        {
            'categories': categories,
        }
    )


# =========================================================
# PRODUCT LIST
# =========================================================

def product_list(request):

    products = Product.objects.filter(
        is_active=True
    ).select_related('category')

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    q = request.GET.get('q', '').strip()

    if q:

        products = products.filter(
            Q(name__icontains=q) |
            Q(author__icontains=q) |
            Q(brand__icontains=q) |
            Q(sku__icontains=q)
        )

    # -----------------------------------------------------
    # Category Filter
    # -----------------------------------------------------

    category = request.GET.get(
        'category',
        ''
    ).strip()

    if category:

        products = products.filter(
            category__slug=category
        )

    # -----------------------------------------------------
    # Categories
    # -----------------------------------------------------

    categories = Category.objects.filter(
        is_active=True
    ).prefetch_related(
        Prefetch(
            'products',
            queryset=Product.objects.filter(
                is_active=True
            ).order_by('-created_at'),
            to_attr='active_products'
        )
    ).order_by('name')

    template_name = (
        'products/list.html'
        if q or category
        else 'products/grouped.html'
    )

    return render(
        request,
        template_name,
        {
            'products': products,
            'categories': categories,
            'q': q,
            'category': category,
        }
    )


# =========================================================
# PRODUCT DETAIL
# =========================================================

def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True
    )

    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(
        id=product.id
    ).order_by('-created_at')[:8]

    return render(
        request,
        'products/detail.html',
        {
            'product': product,
            'related_products': related_products,
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    # -----------------------------------------------------
    # Check Stock
    # -----------------------------------------------------

    if product.stock <= 0:

        messages.error(
            request,
            f'{product.name} বর্তমানে Out of Stock।'
        )

        return redirect('cart')


    # -----------------------------------------------------
    # Get Existing Cart
    # -----------------------------------------------------

    cart = request.session.get(
        'cart',
        {}
    )

    product_id = str(product.id)

    current_quantity = cart.get(
        product_id,
        0
    )


    # -----------------------------------------------------
    # Stock Limit Check
    # -----------------------------------------------------

    if current_quantity + 1 > product.stock:

        messages.warning(
            request,
            f'{product.name} এর available stock মাত্র '
            f'{product.stock} টি।'
        )

        return redirect('cart')


    # -----------------------------------------------------
    # Add Product
    # -----------------------------------------------------

    cart[product_id] = (
        current_quantity + 1
    )

    request.session['cart'] = cart

    request.session.modified = True


    messages.success(
        request,
        f'{product.name} cart-এ যোগ হয়েছে।'
    )

    return redirect('cart')


# =========================================================
# CART
# =========================================================

def cart(request):

    cart_data = request.session.get(
        'cart',
        {}
    )

    items = []

    total = 0


    # -----------------------------------------------------
    # Empty Cart
    # -----------------------------------------------------

    if not cart_data:

        return render(
            request,
            'cart/cart.html',
            {
                'items': [],
                'total': 0,
            }
        )


    # -----------------------------------------------------
    # Cart Items
    # -----------------------------------------------------

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )


        # -------------------------------------------------
        # Prevent Invalid Quantity
        # -------------------------------------------------

        if quantity <= 0:

            continue


        # -------------------------------------------------
        # If Stock Changed
        # -------------------------------------------------

        if quantity > product.stock:

            quantity = product.stock

            cart_data[str(product.id)] = quantity


        # -------------------------------------------------
        # Product Out of Stock
        # -------------------------------------------------

        if product.stock <= 0:

            continue


        # -------------------------------------------------
        # Subtotal
        # -------------------------------------------------

        subtotal = (
            product.current_price *
            quantity
        )

        total += subtotal


        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })


    # Save corrected cart
    request.session['cart'] = cart_data

    request.session.modified = True


    return render(
        request,
        'cart/cart.html',
        {
            'items': items,
            'total': total,
        }
    )


# =========================================================
# UPDATE CART QUANTITY
# =========================================================

@require_POST
def update_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    cart = request.session.get('cart', {})
    product_key = str(product.id)
    current_quantity = int(cart.get(product_key, 0))
    action = request.POST.get('action')

    if action == 'increment':
        quantity = current_quantity + 1
    elif action == 'decrement':
        quantity = current_quantity - 1
    else:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            messages.error(request, 'Please enter a valid quantity.')
            return redirect('cart')

    if quantity <= 0:
        cart.pop(product_key, None)
        messages.success(request, 'Product removed from cart.')
    elif quantity > product.stock:
        messages.warning(
            request,
            f'{product.name} এর available stock মাত্র {product.stock} টি।'
        )
        return redirect('cart')
    else:
        cart[product_key] = quantity
        messages.success(request, 'Cart quantity updated.')

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(
    request,
    product_id
):

    cart = request.session.get(
        'cart',
        {}
    )

    cart.pop(
        str(product_id),
        None
    )

    request.session['cart'] = cart

    request.session.modified = True


    messages.success(
        request,
        'Product cart থেকে remove করা হয়েছে।'
    )

    return redirect('cart')


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # Already logged in
    if request.user.is_authenticated:

        return redirect('home')


    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )


            # Redirect to requested page
            next_url = request.POST.get(
                'next',
                ''
            )


            if next_url:

                return redirect(
                    next_url
                )


            messages.success(
                request,
                'আপনি সফলভাবে Login করেছেন।'
            )

            return redirect('home')


        messages.error(
            request,
            'Username অথবা password সঠিক নয়।'
        )


    next_url = request.GET.get(
        'next',
        ''
    )


    return render(
        request,
        'accounts/login.html',
        {
            'next': next_url
        }
    )


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:

        return redirect('home')


    if request.method == 'POST':

        form = RegistrationForm(
            request.POST
        )


        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                'Account সফলভাবে তৈরি হয়েছে।'
            )

            return redirect('home')


    else:

        form = RegistrationForm()


    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        'আপনি সফলভাবে Logout করেছেন।'
    )

    return redirect('home')


# =========================================================
# CHECKOUT
# =========================================================

@login_required(login_url='login')
def checkout(request):

    cart_data = request.session.get(
        'cart',
        {}
    )


    # -----------------------------------------------------
    # Empty Cart
    # -----------------------------------------------------

    if not cart_data:

        messages.warning(
            request,
            'আপনার cart খালি।'
        )

        return redirect('products')


    items = []

    total = 0


    # -----------------------------------------------------
    # Validate Cart Stock
    # -----------------------------------------------------

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )


        # Invalid quantity
        if quantity <= 0:

            messages.error(
                request,
                f'{product.name} এর quantity সঠিক নয়।'
            )

            return redirect('cart')


        # Stock check
        if quantity > product.stock:

            messages.error(
                request,
                f'{product.name} এর stock মাত্র '
                f'{product.stock} টি।'
            )

            return redirect('cart')


        subtotal = (
            product.current_price *
            quantity
        )

        total += subtotal


        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })


    # =====================================================
    # PLACE ORDER
    # =====================================================

    if request.method == 'POST':

        # -------------------------------------------------
        # Customer Information
        # -------------------------------------------------

        name = request.POST.get(
            'name',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        country = request.POST.get(
            'country',
            'Bangladesh'
        ).strip()

        district = request.POST.get(
            'district',
            ''
        ).strip()

        thana = request.POST.get(
            'thana',
            ''
        ).strip()

        address = request.POST.get(
            'address',
            ''
        ).strip()

        order_note = request.POST.get(
            'order_note',
            ''
        ).strip()


        # -------------------------------------------------
        # Payment Information
        # -------------------------------------------------

        payment_method = request.POST.get(
            'payment_method',
            ''
        ).strip()

        payment_number = request.POST.get(
            'payment_number',
            ''
        ).strip()

        transaction_id = request.POST.get(
            'transaction_id',
            ''
        ).strip()

        payment_screenshot = request.FILES.get(
            'payment_screenshot'
        )


        # =================================================
        # VALIDATION
        # =================================================

        if not name:

            messages.error(
                request,
                'আপনার নাম দিন।'
            )

            return redirect('checkout')


        if not phone:

            messages.error(
                request,
                'Phone number দিন।'
            )

            return redirect('checkout')


        if not email:

            messages.error(
                request,
                'Email address দিন।'
            )

            return redirect('checkout')


        if not district:

            messages.error(
                request,
                'District নির্বাচন করুন।'
            )

            return redirect('checkout')


        if not thana:

            messages.error(
                request,
                'Thana / Upazila দিন।'
            )

            return redirect('checkout')


        if not address:

            messages.error(
                request,
                'Full address দিন।'
            )

            return redirect('checkout')


        # -------------------------------------------------
        # Payment Method Validation
        # -------------------------------------------------

        allowed_payment_methods = [
            'cod',
            'bkash',
            'nagad',
            'rocket',
            'upay',
        ]


        if payment_method not in allowed_payment_methods:

            messages.error(
                request,
                'সঠিক Payment Method নির্বাচন করুন।'
            )

            return redirect('checkout')


        # -------------------------------------------------
        # Online Payment Validation
        # -------------------------------------------------

        if payment_method != 'cod':

            if not payment_number:

                messages.error(
                    request,
                    'Payment number দিন।'
                )

                return redirect('checkout')


            if not transaction_id:

                messages.error(
                    request,
                    'Transaction ID দিন।'
                )

                return redirect('checkout')


        # -------------------------------------------------
        # Payment Status
        # -------------------------------------------------

        if payment_method == 'cod':

            payment_status = 'pending'

        else:

            payment_status = 'submitted'


        # =================================================
        # CREATE ORDER
        # =================================================

        order_number = (
            'NST'
            +
            timezone.now().strftime(
                '%Y%m%d%H%M%S'
            )
            +
            uuid.uuid4().hex[:5].upper()
        )


        # -------------------------------------------------
        # Database Transaction
        # -------------------------------------------------

        with transaction.atomic():

            # =============================================
            # CREATE ORDER
            # =============================================

            order = Order.objects.create(

                user=request.user,

                order_number=order_number,

                name=name,

                phone=phone,

                email=email,

                country=country,

                district=district,

                thana=thana,

                address=address,

                order_note=order_note,

                payment_method=payment_method,

                payment_number=payment_number,

                transaction_id=transaction_id,

                payment_screenshot=payment_screenshot,

                status='pending',

                payment_status=payment_status,

                total=total
            )


            # =============================================
            # CREATE ORDER ITEMS
            # =============================================

            for item in items:

                product = item['product']

                quantity = item['quantity']

                subtotal = item['subtotal']


                # -----------------------------------------
                # Final Stock Check
                # -----------------------------------------

                if quantity > product.stock:

                    raise ValueError(
                        f'{product.name} এর পর্যাপ্ত stock নেই।'
                    )


                # -----------------------------------------
                # Order Item
                # -----------------------------------------

                OrderItem.objects.create(

                    order=order,

                    product=product,

                    product_name=product.name,

                    quantity=quantity,

                    price=product.current_price,

                    subtotal=subtotal
                )


                # -----------------------------------------
                # Reduce Stock
                # -----------------------------------------

                product.stock -= quantity

                product.save(
                    update_fields=['stock']
                )


        # =================================================
        # CLEAR CART
        # =================================================

        request.session['cart'] = {}

        request.session.modified = True


        messages.success(
            request,
            'আপনার Order সফলভাবে গ্রহণ করা হয়েছে।'
        )


        # =================================================
        # ORDER SUCCESS
        # =================================================

        return redirect(
            'order_success',
            order_number=order.order_number
        )


    # =====================================================
    # CHECKOUT PAGE
    # =====================================================

    return render(
        request,
        'checkout/checkout.html',
        {
            'items': items,
            'total': total,
            'user': request.user,
        }
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required(login_url='login')
def order_success(
    request,
    order_number
):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )


    return render(
        request,
        'order/success.html',
        {
            'order': order
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

@login_required(login_url='login')
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        '-created_at'
    )


    return render(
        request,
        'order/my_orders.html',
        {
            'orders': orders
        }
    )


# =========================================================
# ORDER DETAIL
# =========================================================

@login_required(login_url='login')
def order_detail(
    request,
    order_number
):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )


    return render(
        request,
        'order/details.html',
        {
            'order': order
        }
    )
