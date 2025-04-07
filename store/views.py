from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import CartItem
from cart.views import _cart_id
from store.models import Product, Variation
from category.models import Category
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

def store(request, category_slug=None):
    categories = Category.objects.all()
    products = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=selected_category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    product_count = products.count()
    paginator = Paginator(products, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list

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
        'page_obj': page_obj, 
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    colors = Variation.objects.filter(product=product, variation_category='color')
    sizes = Variation.objects.filter(product=product, variation_category='size')

    context = {
        'product': product,
        'in_cart': in_cart,
        'colors': colors,
        'sizes': sizes
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        else:
            products = Product.objects.all()
        
        product_count = products.count()

        paginator = Paginator(products, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        products = page_obj.object_list

        categories = Category.objects.all()
        sizes = "XS SM LG XXL".split()
        price_ranges = "0 50 100 150 200 500 1000".split()
        price_options = "50 100 150 200 500 1000 2000".split()

        context ={
            'products': products,
            'categories': categories,
            'product_count': product_count,
            'keyword': keyword,
            'sizes': sizes,
            'price_ranges': price_ranges,
            'price_options': price_options,
            'page_obj': page_obj,
        }
    
    return render(request, 'store/store.html', context)
