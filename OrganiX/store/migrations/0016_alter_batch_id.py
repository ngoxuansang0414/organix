# Generated by Django 4.2.7 on 2024-04-25 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0015_alter_stock_move_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batch",
            name="id",
            field=models.TextField(editable=False, primary_key=True, serialize=False),
        ),
    ]