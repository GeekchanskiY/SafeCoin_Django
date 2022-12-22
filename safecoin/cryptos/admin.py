from django.contrib import admin
from .models import Crypto, CryptoNews, CrytoPricePoint


@admin.register(Crypto)
class CryptoAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'image', 'circulating_supply', 'volume', 'market_cap', 'transactions_count',
              'description', 'current_price', 'id')
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    readonly_fields = ('id',)


@admin.register(CrytoPricePoint)
class CryptoPriceAdmin(admin.ModelAdmin):
    fields = ('crypto', 'time', 'price')
    list_display = ('crypto', 'time')


@admin.register(CryptoNews)
class CryptoNewsAdmin(admin.ModelAdmin):
    fields = ('image', 'title', 'text', 'views')
    list_display = ('title',)
    search_fields = ('title',)
