# Generated by Django 4.2.2 on 2023-07-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencies',
            name='code',
            field=models.CharField(max_length=255),
        ),
    ]
