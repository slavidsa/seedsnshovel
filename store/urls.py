
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.store, name='store'),
    path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

] 