# Generated by Django 4.2.7 on 2023-11-24 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_remove_order_payment_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Đang chờ", "Pending"),
                    ("Đang giao hàng", "Out For Shipping"),
                    ("Hoàn thành", "Completed"),
                    ("Đã hủy", "Canceled"),
                ],
                default="Pending",
                max_length=100,
            ),
        ),
    ]
