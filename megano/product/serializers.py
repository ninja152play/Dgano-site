from rest_framework import serializers
from product.models import *


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['src', 'alt']


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['src', 'alt']


class SubcategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()
    class Meta:
        model = SubCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)
    image = CategoryImageSerializer()
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.fullName')

    class Meta:
        model = Review
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductShortSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id',
                  'category',
                  'price',
                  'count',
                  'date',
                  'title',
                  'description',
                  'freeDelivery',
                  'images',
                  'tags',
                  'reviews',
                  'rating'
                  ]

    def get_reviews(self, obj):
        return obj.reviews.count()


class CatalogSerializer(serializers.ModelSerializer):
    items = ProductShortSerializer(many=True)

    class Meta:
        model = Catalog
        fields = ['items', 'currentPage', 'lastPage']


class BasketSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()

    class Meta:
        model = Basket
        fields = ['product']


class SaleItemSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'salePrice', 'dateForm', 'dateTo', 'images']

    def get_images(self, obj):
        return [img.src.url for img in obj.images.all()]


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, partial=True)

    class Meta:
        model = Catalog
        fields = ['items', 'currentPage', 'lastPage']