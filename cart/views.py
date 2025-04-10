from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart, CartItem
from store.models import Product, Variation

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# def add_to_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(cart_id=_cart_id(request))
#         cart.save()

#     try:
#         cart_item = CartItem.objects.get(product=product, cart=cart)
#         if cart_item.quantity < cart_item.product.stock:
#             cart_item.quantity += 1
#             cart_item.save()
     
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
#         cart_item.save()
        
#     return redirect('cart')


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass

    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    # Check if the same product with same variations exists
    is_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        for item in cart_items:
            existing_variation = list(item.variations.all())
            existing_variation.sort(key=lambda x: x.id)
            product_variation.sort(key=lambda x: x.id)
            if existing_variation  == product_variation:
                if item.quantity < item.product.stock:
                    item.quantity += 1
                    item.save()
                break
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            cart_item.variations.set(product_variation)
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.variations.set(product_variation)
        cart_item.save()

    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__cart_id=_cart_id(request))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__cart_id=_cart_id(request))
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def increment_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__cart_id=_cart_id(request))
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (total * 2) / 100
        grand_total = total + tax
    except Cart.DoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


