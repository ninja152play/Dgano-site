from django.urls import path, include

from product.views import *

app_name = 'product'

urlpatterns = [
    path('product/<int:pk>', ProductView.as_view(), name='product'),
    path('product/<int:pk>/reviews', ProductReviewView.as_view(), name='review'),
    path('tags', TagsView.as_view(), name='tags'),
    path('categories', CategoriesView.as_view(), name='categories'),
    path('catalog', CatalogView.as_view(), name='catalog'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('products/popular', ProductPopularView.as_view(), name='popular'),
    path('products/limited', ProductLimitedView.as_view(), name='limited'),
    path('basket', BasketView.as_view(), name='basket'),
    path('sales', SaleView.as_view(), name='sale'),
    path('banners', BannersView.as_view(), name='banners'),
]