# Generated by Django 4.2.7 on 2023-11-23 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0003_alter_currency_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=15, max_digits=30),
        ),
    ]