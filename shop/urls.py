from django.urls import path
from django.contrib.auth import views as auth_views
from shop import views
from .views import ProductList

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login_custom'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('process-payment/', views.initiate_payment, name='process_payment'),
    path('success/', views.order_success, name='order_success'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe-webhook'),
    path('dashboard/', views.order_dashboard, name='order_dashboard'),
    path('subscribe/<str:plan_name>/', views.subscribe, name='subscribe'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/products/', views.get_products, name='get_products'),
    path("products/", ProductList.as_view())
    path('api/user/', views.get_current_user, name='get_current_user'),

]