# Generated by Django 4.2.7 on 2024-06-02 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0026_remove_stock_batch_delete_test1_batch_quantity_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderitem",
            old_name="stock",
            new_name="batch",
        ),
    ]
