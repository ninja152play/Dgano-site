MEGANO — сайт магазина, основанный на фреймворке Django.
==================================================

На сайте предоставлены такие возможности, как:
- Просмотр каталога
- Фильтрация по различным параметрам
- Просмотр по категориям и подкатегориям товаров
- Просмотр товаров со скидкой в отдельном разделе
- Регистрация и настройка профиля
- Наполнение корзины и оформление заказа

Установка
=========

1. ```git clone https://github.com/ninja152play/Dgano-site.git```
2. ```cd Django-site```
3. ```docker build -t django-app .```

Запуск
======

```
docker run -d -p 8000:8000 --restart unless-stopped django-app
```

Документация
============
Авторизация и ацетификация построена на sessions и cookies

Создание админа
```
docker ps -a # сопируем CONTAINER ID

docker exec -it CONTAINER ID /bin/bash

cd megano

python manage.py createsuperuser

exit
```
Доступ в админ-панель по ссылке http://server_ip:8000/admin