# Generated by Django 4.1.3 on 2022-12-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptos', '0002_cryptonews_crypto_description_crypto_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptonews',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
