from rest_framework import serializers
from .models import Crypto, CryptoNews, CrytoPricePoint


class CryptoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('name', 'code', 'image', 'description', 'current_price')
        model = Crypto
        read_only_fields = ('current_price',)


class CryptoSearchSerializer(serializers.Serializer):
    search = serializers.CharField(allow_null=True, allow_blank=True)


class CryptoNewsSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CryptoNews
        fields = ('id', 'image', 'title', 'created_at', 'updated_at', 'text', 'views')
