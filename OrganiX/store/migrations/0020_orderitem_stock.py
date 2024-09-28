# Generated by Django 4.2.7 on 2024-05-28 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0019_alter_category_image_alter_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="stock",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="store.stock"
            ),
            preserve_default=False,
        ),
    ]
