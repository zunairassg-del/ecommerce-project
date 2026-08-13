from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from .models import Product, Cart, CartItem, Order
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer
from django.http import JsonResponse

def get_current_user(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "is_authenticated": True,
            "username": request.user.username,
            "email": request.user.email
        })
    else:
        return JsonResponse({
            "is_authenticated": False,
            "message": "User not logged in or guest mode"
        }, status=200)

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer







@api_view(['GET'])
def get_products(request):
    # Abhi ke liye simple data return kar rahe hain
    data = {"message": "Success", "products": ["Laptop", "Phone", "Watch"]}
    return Response(data)







stripe.api_key = settings.STRIPE_SECRET_KEY





# shop/views.py

def initiate_payment(request):
    # Session se dictionary wali list lein
    cart_items = request.session.get('cart', [])
    
    # Yahan sirf 'id' ki list nikalen (Fixed Line)
    cart_ids = [item.get('id') for item in cart_items if item.get('id')]
    
    # Ab filter sahi chalega
    products = Product.objects.filter(id__in=cart_ids)
    
    # Total calculation
    subtotal = sum(float(product.price) for product in products)
    delivery_charges = 500
    grand_total = subtotal + delivery_charges
    stripe_amount = int(grand_total * 100)

    # Stripe session creation
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'pkr',
                'product_data': {
                    'name': 'Order Payment',
                },
                'unit_amount': stripe_amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/', 
        cancel_url='http://127.0.0.1:8000/checkout/', 
    )
    
    return redirect(session.url, code=303)
def payment_success(request):
    request.session['cart'] = {}
    return render(request, 'shop/order_success.html')

# --- Authentication ---

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # User ko get karein
            user = form.get_user()
            # User ko login karein
            login(request, user)
            # Login hone ke baad redirect karein (e.g., 'home' page par)
            return redirect('home') 
        else:
            # Agar form valid nahi hai (wrong password/username)
            # Toh error messages automatically form mein aa jayenge
            pass
    else:
        form = AuthenticationForm()
    
    return render(request, 'shop/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')



def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})




def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Session cart initialize karein
    if 'cart' not in request.session:
        request.session['cart'] = []

    cart = request.session['cart']
    
    # HTML ke hisaab se keys set karein
    item = {
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        # Yahan .url ka access tabhi hoga agar image field ho
        'image_url': product.image.url
    }
    
    cart.append(item)
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))
def view_cart(request):
    cart_items = request.session.get('cart', [])
    
    # Sirf wahi items rakhein jin mein 'id' valid hai
    valid_cart_items = [item for item in cart_items if item.get('id')]
    
    # Agar items remove huyi hain, to session update karein
    if len(valid_cart_items) != len(cart_items):
        request.session['cart'] = valid_cart_items
        request.session.modified = True
        
    total = sum(float(item.get('price', 0)) for item in valid_cart_items)
    
    return render(request, 'shop/view_cart.html', {
        'products': valid_cart_items, 
        'total': total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    
    # Cart mein se item dhoondein aur remove karein
    updated_cart = [item for item in cart if item.get('id') != product_id]
    
    # Session update karein
    request.session['cart'] = updated_cart
    request.session.modified = True
    
    return redirect('view_cart')
def checkout(request):
    # Session se cart data lein
    cart_items = request.session.get('cart', [])
    
    # Session mein se sirf 'id's ki list nikalen
    cart_ids = [item.get('id') for item in cart_items if item.get('id')]
    
    # Ab database filter sahi chalega
    products = Product.objects.filter(id__in=cart_ids)
    total_price = sum(float(product.price) for product in products)

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Order create karein
        Order.objects.create(name=name, address=address, phone=phone, total_price=total_price)
        
        # Cart khali karein
        request.session['cart'] = []
        request.session.modified = True
        
        return render(request, 'shop/order_success.html')

    return render(request, 'shop/checkout.html', {'total': total_price})

def process_payment(request):
    if request.method == 'POST':
        method = request.POST.get('payment_method')
        
        if method == 'stripe':
            return redirect('initiate_payment')
        elif method == 'cod':
            return redirect('payment_success')
    return redirect('checkout')


def order_success(request):
      return render(request, 'shop/success.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Jab payment success ho jaye
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Yahan apna logic likhen, jaise:
        # order = Order.objects.get(stripe_session_id=session.id)
        # order.paid = True
        # order.save()

    return HttpResponse(status=200)



def order_dashboard(request):
    # Sirf login user ke orders nikalen
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_dashboard.html', {'orders': orders})



SUBSCRIPTION_PLANS = {
    'pro_monthly': 'price_1TsJlHPJpfupxSWqZa1TD1t',
    'pro_yearly': 'price_1TsJmKPJpfupxSWqf6KwmhCA',
    'plus_monthly': 'price_1TsJpuPJpfupxSWqpREAfmF6',
    'plus_yearly': 'price_1TsJqaPJpfupxSWqp3KUskSZ',
}

def subscribe(request, plan_name):
    price_id = SUBSCRIPTION_PLANS.get(plan_name)
    
    if not price_id:
        return HttpResponse("Invalid Plan selected!", status=400)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
        return redirect(session.url)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
def pricing_view(request):
    return render(request, 'shop/pricing.html')

def delete_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('view_cart')