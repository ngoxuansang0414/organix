# Generated by Django 4.2.7 on 2023-12-08 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('momo', '0004_paymentinfo_resultcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentinfo',
            name='refund_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='transId',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]