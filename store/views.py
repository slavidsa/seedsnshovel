from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    
    if category_slug != None:
        categories=get_object_or_404(Category, slug=category_slug)
        products=Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    
    context = {
        'products': paged_products,
    }
    return render(request, 'store/store.html',context)


def product_detail(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    related_products = Product.objects.filter(category=single_product.category).exclude(slug=product_slug)
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your Review has been recorded.')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
        return redirect(url)

