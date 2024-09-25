from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from shop.form import CustomUserForm, CustomerForm,OrderForm
from django.views.decorators.csrf import csrf_exempt
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from shop.models import Favourite  # Import your Favourite model
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
import logging






# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect('/')
    
def remove_fav(request,fid):
    item=Favourite.objects.get(id=fid)
    item.delete()
    return redirect('/favviewpage')


def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect('/')

    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('/cart')

def fav_page(request):
    if request.headers.get('X-Requested-Width')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)        
            product_id=(data['pid'])
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already Added In Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Products added to favourites'},status=200)
        else:
            return JsonResponse({'status':'Login to add products to favourites'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)




def add_to_cart(request):
    if request.headers.get('X-Requested-Width')=='XMLHttpRequest':
        if request.user.is_authenticated:
      
            data=json.load(request) 
            
            product_qty=data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already Added In Cart'},status=200)
                else:
                    if product_status.quantity >=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        # Calculate total items in cart
                        
                        return JsonResponse({'status':'Product added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock not available currently!'},status=200)

        else:
            return JsonResponse({'status':'Login to add products to the cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)



# ashmitha made this cart_count too
def cart_count(request):
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0
    return JsonResponse({'cart_item_count': cart_item_count})    

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully!") 
    return redirect('/') 

def login_page(request):
    if request.user.is_authenticated:
          return redirect('/') 
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully!")  
                return redirect('/') 
            else:
                messages.error(request,"Invalid Username Or Password")   
                return redirect('/login')
        
        return render(request,"shop/login.html")

def register(request):
    form =CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"You Have Registered Successfully! You Can Now Login")
            return redirect('/login')
        else:
            print(form.errors)
        
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    category = Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category": category})

def collectionsview(request,name):

    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,"shop/products/index.html",{"products": products,"category_name":name})
    else:
        messages.warning(request,"NO Such Category Found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No Such Product Found")
            return redirect('collections')
    else:
        messages.error(request,"NO Such Category Found")
        return redirect('collections')

# # ashmitha here made the changes created new def get_cart_count   
# def get_cart_count(request):
#     if request.user.is_authenticated:
#         cart_count = Cart.objects.filter(user=request.user).count()
#         return JsonResponse({'cart_count': cart_count}, status=200)
#     else:
#         return JsonResponse({'cart_count': 0}, status=200)

# ashmitha added get_favoru _count

@login_required
def get_favourite_count(request):
    favourite_count = Favourite.objects.filter(user=request.user).count()
    return JsonResponse({'fav_count': favourite_count})


# razorpay_client = razorpay.Client(auth=('rzp_test_hTqiwdw1Toqsks','98X6I2YhJKfiJo2hGyiSiqos' ))

# def initiate_payment(request):
#     if request.method == 'POST':
#         amount = int(request.POST['amount']) * 100  # amount in paisa
#         currency = 'INR'

#         payment_order = razorpay_client.order.create({
#             'amount': amount,
#             'currency': currency,
#             'payment_capture': '1'  # auto-capture
#         })

#         order_id = payment_order['id']
#         order_status = payment_order['status']

#         return JsonResponse({
#             'order_id': order_id,
#             'status': order_status,
#             'amount': amount // 100,
#             'currency': currency
#         })

#     return render(request, 'payment.html')
def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_amount = sum(item.total_cost for item in cart_items)
        customer_form = CustomerForm()  # Instantiate CustomerForm

        context = {
            'cart': cart_items,
            'total_amount': total_amount,
            'customer_form': customer_form,  # Pass CustomerForm to context
        }
        
        return render(request, 'shop/checkout.html', context)
    else:
        # Handle case where user is not authenticated (redirect to login or handle accordingly)
        return redirect('login')  # Replace 'login' with your actual login URL
    

razorpay_client = razorpay.Client(auth=('rzp_test_hTqiwdw1Toqsks','98X6I2YhJKfiJo2hGyiSiqos' ))
# def initiate_payment(request):
#     if request.method == 'POST':
#         amount_str = request.POST['amount']
#         amount = int(float(amount_str) * 100)  # Convert to paisa
#         currency = 'INR'

#         # Create the Razorpay order
#         try:
#             payment_order = razorpay_client.order.create({
#                 'amount': amount,
#                 'currency': currency,
#                 'payment_capture': '1'  # Auto-capture payment
#             })

#             order_id = payment_order['id']
#             order_status = payment_order['status']
#             short_url = payment_order['short_url']

#             # Redirect user to Razorpay checkout page
#             return redirect(short_url)

#         except Exception as e:
#             return render(request, 'shop/payment_error.html', {'error': str(e)})

#     return render(request, 'checkout.html')


def initiate_payment(request):
    if request.method == 'POST':
        try:
            amount_str = request.POST['amount']  # Assuming amount is passed as a string
            # Convert the amount string to a float first to handle decimal values
            amount_float = float(amount_str)
            # Convert to paisa or smallest currency unit
            amount_paisa = int(amount_float * 100)  # Convert to integer paisa
            currency = 'INR'  # Assuming currency is INR

            payment_order = razorpay_client.order.create({
                'amount': amount_paisa,
                'currency': currency,
                'payment_capture': '1'  # auto-capture
            })

            order_id = payment_order['id']
            order_status = payment_order['status']

            return JsonResponse({
                'order_id': order_id,
                'status': order_status,
                'amount': amount_paisa // 100,  # converting back to rupees
                'currency': currency
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)

# def initiate_payment(request):
#     if request.method == 'POST':
#         amount_str = request.POST['amount']  # Fetch amount as string
#         amount = int(float(amount_str) * 100)
#         currency = 'INR'

#         payment_order = razorpay_client.order.create({
#             'amount': amount,
#             'currency': currency,
#             'payment_capture': '1'  # auto-capture
#         })

#         order_id = payment_order['id']

#         return redirect(payment_order['short_url'])  # Redirect user to Razorpay checkout page

#     return render(request, 'checkout.html')


# razorpay_client = razorpay.Client(auth=('rzp_test_hTqiwdw1Toqsks','98X6I2YhJKfiJo2hGyiSiqos' ))
# def initiate_payment(request):
#     if request.method == 'POST':
#         try:
#             amount_str = request.POST['amount']
#             amount = int(float(amount_str) * 100)
#             currency = 'INR'

#             payment_order = razorpay_client.order.create({
#                 'amount': amount,
#                 'currency': currency,
#                 'payment_capture': '1'
#             })

#             order_id = payment_order['id']
#             order_status = payment_order['status']
#             # short_url = payment_order.get('short_url')  # Access 'short_url' if it exists in the response

#             return JsonResponse({
#                 'order_id': order_id,
#                 'status': order_status,
#                 'amount': amount // 100,
#                 'currency': currency,
#                 # 'short_url': short_url  # Include 'short_url' in the JSON response if available
#             })

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return render(request, 'payment.html')


# @login_required
# def initiate_payment(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total_amount = sum(item.total_cost for item in cart_items)

#     if request.method == 'POST':
#         customer_form = CustomerForm(request.POST)
#         if customer_form.is_valid():
#             customer = customer_form.save(commit=False)
#             customer.user = request.user
#             customer.save()

#             order = Order.objects.create(customer=customer, total_amount=total_amount)

#             for item in cart_items:
#                 OrderItem.objects.create(order=order, product=item.product, quantity=item.product_qty, price=item.total_cost)

#             # Create Razorpay order
#             client = razorpay.Client(auth=('rzp_test_vEfFAwxQPId72J', 'uw9U8NNnBZDZYEJp0jUHUef7'))
#             razorpay_order = client.order.create({
#                 "amount": int(order.total_amount * 100),  # Amount in paise
#                 "currency": "INR",
#                 "payment_capture": "1"
#             })
#             order.razorpay_order_id = razorpay_order['id']
#             order.save()

#             # Store the Razorpay order ID and amount in the session
#             request.session['razorpay_order_id'] = razorpay_order['id']
#             request.session['amount'] = order.total_amount * 100

#             # Redirect to the payment page
#             return redirect('payment_page')

#     else:
#         customer_form = CustomerForm()

#     context = {
#         'customer_form': customer_form,
#         'cart': cart_items,
#         'total_amount': total_amount
#     }
#     return render(request, 'shop/checkout.html', context)



# def initiate_payment(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')

#         try:
#             product = Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             return JsonResponse({'error': f'Product with id {product_id} does not exist.'}, status=404)

#         # Example: Create an OrderItem associated with the product
#         order_item = OrderItem.objects.create(
#             product=product,
#             quantity=1,  # Example quantity
#             price=product.selling_price  # Example price
#         )

#         # Continue with your payment initiation logic
#         return redirect('payment_success')  # Replace with your actual success URL

#     else:
#        return render(request, 'shop/checkout.html',)


# @csrf_exempt
# def complete_payment(request):
#     if request.method == 'POST':
#         data = request.POST
#         try:
#             razorpay_client.utility.verify_payment_signature(data)
#             # Update your database and handle success scenario
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'failed'})
#     return redirect('payment_failed_url')

@csrf_exempt
def complete_payment(request):
    if request.method == 'POST':
        data = request.POST
        try:
            razorpay_client.utility.verify_payment_signature(data)
            order_id = data['razorpay_order_id']
            payment_id = data['razorpay_payment_id']

            # Retrieve order from database using order_id stored in session
            order = Order.objects.get(id=request.session.get('order_id'))
            order.payment_status = 'Paid'
            order.save()

            # Perform further actions as per your application's logic (e.g., send confirmation emails, update inventory)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = request.POST
        try:
            razorpay_client.utility.verify_payment_signature(data)
            order_id = data['razorpay_order_id']
            payment_id = data['razorpay_payment_id']

            # Retrieve order from database using order_id stored in session
            order = Order.objects.get(id=request.session.get('order_id'))
            order.payment_status = 'Paid'
            order.save()

            # Perform further actions as per your application's logic (e.g., send confirmation emails, update inventory)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})
    return JsonResponse({'status': 'invalid request'})






# @csrf_exempt
# def payment_success(request):
#     razorpay_payment_id = request.GET.get('razorpay_payment_id')
#     razorpay_order_id = request.GET.get('razorpay_order_id')

#     # Verify payment (optional but recommended)
#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     try:
#         payment = client.payment.fetch(razorpay_payment_id)
#         if payment['status'] == 'captured':
#             # Update order status in database, send confirmation email, etc.
#             return render(request, 'shop/payment_success.html', {})
#     except razorpay.errors.BadRequestError as e:
#         return redirect('payment_failure')

#     return redirect('payment_failure')


# def payment_failure(request):
#     # Handle payment failure
#     return render(request, 'shop/failure.html')



