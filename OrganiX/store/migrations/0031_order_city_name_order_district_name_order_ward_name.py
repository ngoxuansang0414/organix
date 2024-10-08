# Generated by Django 4.2.7 on 2024-09-17 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0030_alter_cart_options_alter_cart_account_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="city_name",
            field=models.CharField(
                default="Tỉnh Hưng Yên", max_length=100, verbose_name="Tỉnh/Thành phố"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="district_name",
            field=models.CharField(
                default="Huyện Văn Lâm", max_length=100, verbose_name="Quận/Huyện"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="ward_name",
            field=models.CharField(
                default="Xã Đình Dù", max_length=100, verbose_name="Xã/Phường"
            ),
            preserve_default=False,
        ),
    ]
