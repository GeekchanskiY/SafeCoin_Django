from rest_framework import serializers
from .models import SCUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'username', 'email', 'birthday', 'about_me', 'avatar', )
        model = SCUser
        read_only_fields = ('id',)
