from cart.views import _cart_id
from .models import Cart, CartItem

def counter(request):
    cart_count = 0

    # Skip admin pages
    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
            cart_items = CartItem.objects.filter(cart=cart, is_active=True) if cart else []

        cart_count = sum(item.quantity for item in cart_items)

    except Exception as e:
        cart_count = 0

    return {'cart_count': cart_count}
