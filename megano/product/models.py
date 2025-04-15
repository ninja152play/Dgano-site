from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import Profile

# Create your models here.
class ProductImage(models.Model):
    """Модель изображения продукта"""
    src = models.ImageField(upload_to='app_shop/products/',
                            default='app_shop/products/default.png',
                            verbose_name='Ссылка'
                            )
    alt = models.CharField(max_length=255, verbose_name='Альтернативный текст')

    class Meta:
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продуктов'


class CategoryImage(models.Model):
    """Модель изображения категории"""
    src = models.ImageField(upload_to='app_shop/categories/',
                            default='app_shop/categories/default.png',
                            verbose_name='Ссылка'
                            )
    alt = models.CharField(max_length=255, verbose_name='Альтернативный текст')

    class Meta:
        verbose_name = 'Изображение категории'
        verbose_name_plural = 'Изображения категорий'


class Tag(models.Model):
    """Модель тега продукта"""
    name = models.CharField(max_length=255, verbose_name='Название')
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class SubCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ForeignKey(CategoryImage, on_delete=models.CASCADE, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ForeignKey(CategoryImage, on_delete=models.CASCADE,verbose_name='Изображение')
    subcategories = models.ManyToManyField(SubCategory, verbose_name='Подкатегории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Review(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='E-mail', blank=True)
    text = models.TextField(verbose_name='Текст')
    rate = models.PositiveIntegerField(verbose_name='Оценка', default=0)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Specification(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    value = models.CharField(max_length=255, verbose_name='Значение')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class Product(models.Model):
    """Модель продукта"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.PositiveIntegerField(verbose_name='Количество', default=0)
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    fullDescription = models.TextField(verbose_name='Подробное описание')
    freeDelivery = models.BooleanField(verbose_name='Бесплатная доставка')
    limited = models.BooleanField(verbose_name='Ограниченный товар', default=False)
    images = models.ManyToManyField(ProductImage, verbose_name='Изображения')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    reviews = models.ManyToManyField(Review, verbose_name='Отзывы', blank=True)
    specifications = models.ManyToManyField(Specification, verbose_name='Характеристики')
    rating = models.FloatField(
                                blank=True,
                                verbose_name='Рейтинг',
                                default=0.0,
                                validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Скидка', null=True, blank=True)
    dateForm = models.DateField(verbose_name='Дата начала скидки', null=True, blank=True)
    dateTo = models.DateField(verbose_name='Дата окончания скидки', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Catalog(models.Model):
    """Модель каталога товаров !!!ЯВЛЯЕТСЯ КЛАССОМ ДЛЯ СЕРЕАЛИЗАЦИИ!!!"""
    items = models.ManyToManyField(Product, verbose_name='Товары')
    currentPage = models.PositiveIntegerField(verbose_name='Текущая страница', default=1)
    lastPage = models.PositiveIntegerField(verbose_name='Последняя страница')

    class Meta:
        verbose_name = 'Каталог'


class Basket(models.Model):
    """Модель корзины покупок"""
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товары')
    count = models.PositiveIntegerField(verbose_name='Количество', default=1)



