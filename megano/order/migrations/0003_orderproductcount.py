# Generated by Django 5.1.7 on 2025-03-22 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_payment_options'),
        ('product', '0008_product_dateform_product_dateto_product_saleprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProductCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'Количество товаров в заказе',
            },
        ),
    ]
