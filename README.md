# MEGANO — # Интернет-магазин Django REST API

![Django](https://img.shields.io/badge/Django-3.2-green)
![DRF](https://img.shields.io/badge/DRF-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-purple)

Полнофункциональный backend для интернет-магазина с REST API на Django.

## 📌 Основные модули

### 1. Пользователи (`user`)
- Регистрация/авторизация
- Профиль с аватаром
- Смена пароля
- JWT-аутентификация

### 2. Каталог товаров (`product`)
- Древовидные категории
- Фильтрация и сортировка
- Теги и характеристики
- Отзывы и рейтинги
- Система скидок

### 3. Корзина и заказы (`order`)
- Управление корзиной
- Оформление заказов
- Разные способы оплаты
- История заказов

## 🛠 Технологии

- **Python 3.9+**
- **Django 3.2**
- **Django REST Framework**
- **PostgreSQL**
- **Docker** (опционально)

## 🚀 Быстрый старт

### 1. Установка
```bash
git clone https://github.com/ninja152play/Dgano-site.git
cd Dgano-site
```
### 2. Настройка БД
Отредактируйте settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop_db',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## 🐳 Docker-развертывание
```bash
docker-compose up --build
```
## 🌐 Основные эндпоинты
Модуль	

Метод	Путь	              Описание

Пользователи	
- POST	/api/sign-in	      Авторизация
- POST	/api/sign-up	      Регистрация
- POST  /api/sign-out         Выход
- GET   /api/profile          Профиль
- POST  /api/profile/password Смена пароля
- POST  /api/profile/avatar   Смена аватарки

Продукты
- GET	/api/catalog	Фильтруемый каталог
- GET	/api/product/{id}	Детали товара
- GET   /api/tags Получение тегов
- GET   /api/categories Получение категорий
- GET   /api/products/popular Получение популярных товаров
- GET   /api/products/limited Получение лимитированных товаров
- GET   /api/basket Получение корзины
- POST   /api/basket Добавление товара в корзину
- DELETE   /api/basket Удаление товара из корзины
- GET   /api/sales Получение товаров с распродажи
- GET   /api/banners Получение банеров

Заказы	
- POST	/api/orders	Создать заказ
- GET	/api/order/{id}	Детали заказа
- POST  /api/payment/{id} Создание оплаты

# Создание админа
```
docker ps -a # копируем CONTAINER ID

docker exec -it CONTAINER ID /bin/bash

cd megano

python manage.py createsuperuser

exit
```
