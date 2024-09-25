# ashmitha made changes

# from .models import Cart

# def cart_item_count(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user, checked_out=False).first()
#         if cart:
#             return {'cart_item_count': cart.items.count()}
#     return {'cart_item_count': 0}


# shop/context_processors.py

from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_item_count = 0
    return {
        'cart_item_count': cart_item_count
    }
