# Generated by Django 5.1.6 on 2025-03-20 16:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0009_product_re_seller_price_product_retail_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
