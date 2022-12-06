# Generated by Django 4.1.3 on 2022-12-06 02:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cryptos', '0003_cryptonews_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptonews',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cryptonews',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
