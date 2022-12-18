from django.db import models

# Create your models here.


class Crypto(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="cryptos/", null=True)
    description = models.TextField(null=True, blank=True)
    volume = models.FloatField(default=0.0)
    circulating_supply = models.FloatField(default=0.0)
    market_cap = models.FloatField(default=0.0)
    transactions_count = models.IntegerField(default=0)
    current_price = models.FloatField()

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.name} {self.code}'

    class Meta:
        verbose_name = 'CryptoCurrency'
        verbose_name_plural = 'CryptoCurrencies'


class CrytoPricePoint(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    time = models.DateTimeField()
    price = models.FloatField()

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{str(self.crypto)} price is {self.price} at {str(self.time)}'


class CryptoNews(models.Model):
    image = models.ImageField(upload_to="news/", null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{str(self.title)}'
    