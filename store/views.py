from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from category.models import Category

# Create your views here.

def store(request, category_slug=None):
    categories = Category.objects.all()
    products = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=selected_category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    product_count = products.count()

    sizes = "XS SM LG XXL".split()
    price_ranges = "0 50 100 150 200 500 1000".split()
    price_options = "50 100 150 200 500 1000 2000".split()

    context = {
        'categories': categories,
        'products': products,
        'product_count': product_count,
        'sizes': sizes,
        'price_ranges': price_ranges,
        'price_options': price_options,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Example logic (customize based on your cart system)
    cart = request.session.get('cart', {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session['cart'] = cart

    return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)