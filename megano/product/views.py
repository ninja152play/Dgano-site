from datetime import datetime

from django.shortcuts import render
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from product.models import *
from product.serializers import *

# Create your views here.
class ProductView(APIView):
    def get(self, request, pk):
        try:
            products = Product.objects.get(pk=pk)
            print(products)
            serializer = ProductSerializer(products)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductReviewView(APIView):
    pass
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = request.data
        print(review)
        return Response({'message': 'Review created'}, status=status.HTTP_200_OK)


class TagsView(APIView):
    def get(self, request):
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoriesView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CatalogView(APIView):
    def get(self, request):
        print(request.GET)
        try:
            filter_name = request.GET.get('filter[name]')#
            filter_min_price = request.GET.get('filter[minPrice]')#
            filter_max_price = request.GET.get('filter[maxPrice]')#
            filter_free_delivery = request.GET.get('filter[freeDelivery]').capitalize()#
            filter_available = request.GET.get('filter[available]')#
            if filter_available == 'true':
                filter_available = True
            else:
                filter_available = False
            sort = request.GET.get('sort')#
            sort_type = request.GET.get('sortType')#
            if sort_type == 'dec':
                sort_type = '-'
            else:
                sort_type = ''
            filter_sort = ''.join(sort_type + sort)
            if sort == 'reviews':
                filter_sort = ''.join(sort_type + 'num_reviews')
            tags = list(request.GET.getlist('tags[]'))
            if not tags == []:
                if filter_available:
                    if filter_name:
                        products = (Product.objects.filter(title=filter_name,
                                                          price__gte=filter_min_price,
                                                          price__lte=filter_max_price,
                                                          freeDelivery=filter_free_delivery,
                                                          count__gte=1,
                                                          tags__in=tags,
                                                          )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
                    else:
                        products = (Product.objects.filter(price__gte=filter_min_price,
                                                          price__lte=filter_max_price,
                                                          freeDelivery=filter_free_delivery,
                                                          count__gte=1,
                                                          tags__in=tags,
                                                          )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
                else:
                    if filter_name:
                        products = (Product.objects.filter(title=filter_name,
                                                          price__gte=filter_min_price,
                                                          price__lte=filter_max_price,
                                                          freeDelivery=filter_free_delivery,
                                                          count__lte=0,
                                                          tags__in=tags,
                                                          )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
                    else:
                        products = (Product.objects.filter(price__gte=filter_min_price,
                                                          price__lte=filter_max_price,
                                                          freeDelivery=filter_free_delivery,
                                                          count__lte=0,
                                                          tags__in=tags,
                                                          )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
            else:
                if filter_available:
                    if filter_name:
                        products = (Product.objects.filter(title=filter_name,
                                                           price__gte=filter_min_price,
                                                           price__lte=filter_max_price,
                                                           freeDelivery=filter_free_delivery,
                                                           count__gte=1,
                                                           )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
                    else:
                        products = (Product.objects.filter(price__gte=filter_min_price,
                                                           price__lte=filter_max_price,
                                                           freeDelivery=filter_free_delivery,
                                                           count__gte=1,
                                                           )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
                else:
                    if filter_name:
                        products = (Product.objects.filter(title=filter_name,
                                                           price__gte=filter_min_price,
                                                           price__lte=filter_max_price,
                                                           freeDelivery=filter_free_delivery,
                                                           count__lte=0,
                                                           )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())
                    else:
                        products = (Product.objects.filter(price__gte=filter_min_price,
                                                           price__lte=filter_max_price,
                                                           freeDelivery=filter_free_delivery,
                                                           count__lte=0,
                                                           )
                                    .annotate(num_reviews=Count('reviews')).order_by(filter_sort).all())

            limit = int(request.GET.get('limit'))
            current_page = int(request.GET.get('currentPage'))
            last_page = int(products.count()/limit)+1
            products = products[(current_page-1)*limit:current_page*limit]
            catalog = {
                'currentPage': current_page,
                'lastPage': last_page,
                'items': products
            }
            serializer = CatalogSerializer(catalog)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductPopularView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all().order_by('rating')[:8]
            serializer = ProductShortSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductLimitedView(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(limited=True)
            serializer = ProductShortSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BasketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user = Profile.objects.get(user=user)
            baskets = Basket.objects.filter(user=user)
            products = []
            for basket in baskets:
                basket.product.count = basket.count
                products.append(basket.product)
            serializer = ProductShortSerializer(products, many=True, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            user = Profile.objects.get(user=user)
            product = request.data['id']
            count = request.data['count']
            product_obj = Product.objects.get(pk=product)
            basket_obj, created = Basket.objects.get_or_create(user=user, product=product_obj)
            if not created:
                basket_obj.count += count
                basket_obj.save()

            serializer = ProductSerializer(product_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            user = request.user
            user = Profile.objects.get(user=user)
            product = request.data['id']
            count = request.data['count']
            product_obj = Product.objects.get(pk=product)
            basket_obj = Basket.objects.get(user=user, product=product_obj)
            basket_obj.count -= count
            if basket_obj.count == 0:
                basket_obj.delete()
            else:
                basket_obj.save()

            serializer = ProductSerializer(product_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BannersView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductShortSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaleView(APIView):
    def get(self, request):
        # try:
            products = (Product.objects.filter(salePrice__isnull=False,
                                               dateForm__lte=datetime.now(),
                                               dateTo__gte=datetime.now(),
                                               )
                        .all())
            current_page = int(request.GET.get('currentPage'))
            last_page = int(products.count() / 20) + 1
            products = products[(current_page - 1) * 20:current_page * 20]
            sale = {
                'currentPage': current_page,
                'lastPage': last_page,
                'items': products
            }
            serializer = SaleSerializer(sale)
            return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception:
#             return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)