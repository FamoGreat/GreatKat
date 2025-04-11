import datetime
import uuid
from django.shortcuts import redirect, render
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from cart.models import CartItem
from order.forms import OrderForm
from order.models import Order, OrderProduct, Payment

# Create your views here.

def mock_payment(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)

        # Create a fake payment
        payment = Payment.objects.create(
            user=request.user,
            payment_id=str(uuid.uuid4()),
            payment_method="MockPayment",
            amount_paid=order.order_total,
            status="Completed",
        )

        order.payment = payment
        order.is_ordered = True
        order.save()

    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    for item in cart_items:
        # Create OrderProduct
        order_product = OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=user,
            product=item.product,
            variation=item.variations.first() if item.variations.exists() else None,
            color=item.variations.filter(variation_category='color').first().variation_value if item.variations.filter(variation_category='color').exists() else '',
            size=item.variations.filter(variation_category='size').first().variation_value if item.variations.filter(variation_category='size').exists() else '',
            quantity=item.quantity,
            product_price=float(item.product.price),
            ordered=True,
        )

        # Reduce stock
        product = item.product
        product.stock -= item.quantity
        product.save()

    # Clear the cart
    cart_items.delete()
    order_products = OrderProduct.objects.filter(order=order)
    sub_total = order.order_total - order.tax

    current_site = get_current_site(request)
    mail_subject = "Thank you for your order"
    message = render_to_string('order/order_email.html', {
        'user': user,
        'order': order,
        'sub_total': sub_total,
        'order_products': order_products,
        'domain': current_site.domain,
    })
    to_email = user.email
    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=message,
        to=[to_email]
    )
    email.attach_alternative(message, "text/html")
    email.send()

    context = {
        "sub_total": sub_total,
        "order": order,
        "payment": payment,
        "order_products": order_products,
    }
    return render(request, 'order/order_complete.html', context)


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    cart_items_count = cart_items.count()
    if cart_items_count <= 0:
        return redirect("store")
    
    tax = 0
    grand_total = 0 
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (total * 2) / 100
    grand_total = total + tax

    form = OrderForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            order = Order()
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address_line_1 = form.cleaned_data['address_line_1']
            order.address_line_2 = form.cleaned_data['address_line_2']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.order_note = form.cleaned_data['order_note']
            order.tax = tax
            order.order_total = grand_total
            order.ip = request.META.get('REMOTE_ADDR')
            order.save()
            
            # order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%d%m')

            order.order_number = current_date + str(order.id)
            order.save()

            new_order = Order.objects.get(user=current_user, is_ordered=False, order_number=order.order_number)
            context = {
                'order': new_order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request,"order/payments.html", context)
    return render(request, 'store/checkout.html')


def order_complete(request):
    # order_number = request.GET.get('order_number')
    # order = Order.objects.get(order_number=order_number)
    # ordered_products = OrderProduct.objects.filter(order_id=order.id)
    # subtotal = 0
    # for i in ordered_products:
    #     subtotal += i.product_price * i.quantity

    # context = {
    #     'order': order,
    #     'ordered_products': ordered_products,
    #     'subtotal': subtotal,
    
    return render(request, 'order/order_complete.html')