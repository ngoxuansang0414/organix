# Generated by Django 4.2.7 on 2023-11-18 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import store.models.products


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='', max_length=150)),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/categories/')),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=Hidden')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=200)),
                ('total_price', models.ImageField(upload_to='')),
                ('payment_method', models.CharField(max_length=50)),
                ('payment_id', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('Pending', 'Đang chờ'), ('Out For Shipping', 'Đang giao hàng'), ('Completed', 'Hoàn thành'), ('Canceled', 'Đã hủy')], default='Pending', max_length=100)),
                ('note', models.TextField(null=True)),
                ('tracking_no', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='', max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('unit', models.CharField(default='sản phẩm', max_length=30)),
                ('original_price', models.IntegerField(default=0)),
                ('sale_price', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to=store.models.products.get_file_path)),
                ('status', models.BooleanField(default=True, help_text='0=default, 1=Hidden')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certification', models.TextField(default='Không rõ')),
                ('origin', models.TextField(default='Không rõ')),
                ('uses', models.TextField(default='Không rõ')),
                ('instructions_for_use', models.TextField(default='Không rõ')),
                ('preserving_instruction', models.TextField(default='Không rõ')),
                ('expiry', models.TextField(default='Không rõ')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_qty', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]