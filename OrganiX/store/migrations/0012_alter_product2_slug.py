# Generated by Django 4.2.7 on 2024-03-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0011_batch_stock_product2_batch_product2"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product2",
            name="slug",
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]
