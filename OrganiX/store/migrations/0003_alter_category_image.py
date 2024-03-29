# Generated by Django 4.2.7 on 2023-11-21 14:10

from django.db import migrations, models
import store.models.categories


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_alter_product_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=store.models.categories.get_file_path
            ),
        ),
    ]
