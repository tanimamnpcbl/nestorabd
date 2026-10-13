from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),

    # Products
    path(
        'products/',
        views.product_list,
        name='products'
    ),

    path(
        'product/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),

    # Cart
    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='cart_add'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.update_cart,
        name='cart_update'
    ),

    path(
        'cart/remove/<int:product_id>/',
        views.remove_from_cart,
        name='cart_remove'
    ),

    # Authentication
    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Checkout
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    # Orders
    path(
        'order/success/<str:order_number>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'order/<str:order_number>/',
        views.order_detail,
        name='order_detail'
    ),
]
