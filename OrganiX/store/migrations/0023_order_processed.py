# Generated by Django 4.2.7 on 2024-06-01 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0022_alter_orderitem_stock"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="processed",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
