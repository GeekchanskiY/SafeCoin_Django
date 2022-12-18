from rest_framework import viewsets
from .serializers import CryptoSerializer, CryptoNewsSerializer, CryptoSearchSerializer
from .models import Crypto, CryptoNews, CrytoPricePoint
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q


class CryptoViewSet(viewsets.ModelViewSet):
    
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    lookup_field = 'name'
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False, name='search', serializer_class=CryptoSearchSerializer)
    def search(self, request):
        data = request.data.get('search', None)
        if data is not None:
            serializer = CryptoSerializer(list(self.queryset.filter(Q(name__contains=data)|Q(code__contains=data))), many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            serializer = CryptoSerializer(list(self.queryset), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class CryptoNewsViewSet(viewsets.ModelViewSet):
    queryset = CryptoNews.objects.all()
    serializer_class = CryptoNewsSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


