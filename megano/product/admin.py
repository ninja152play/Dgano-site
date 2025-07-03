from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(CategoryImage)
admin.site.register(Tag)
admin.site.register(Specification)