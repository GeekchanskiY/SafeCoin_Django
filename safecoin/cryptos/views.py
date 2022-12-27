from rest_framework import viewsets
from .serializers import CryptoSerializer, CryptoNewsSerializer,\
    CryptoSearchSerializer, CryptoPricePointSerializer
from .models import Crypto, CryptoNews, CrytoPricePoint
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q
from rest_framework import pagination
from django.core.exceptions import ObjectDoesNotExist


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
        name = request.data.get('search', None)
        min_price = request.data.get('min_price', None)
        max_price = request.data.get('max_price', None)
        min_cap = request.data.get('min_cap', None)
        max_cap = request.data.get('max_cap', None)

        queryset = self.queryset
        if name is not None:
            queryset = queryset.filter(Q(name__contains=name) | Q(code__contains=name))

        if min_price is not None:
            queryset = queryset.filter(current_price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(current_price__lte=max_price)

        if max_cap is not None:
            queryset = queryset.filter(market_cap__lte=max_cap)

        if min_cap is not None:
            queryset = queryset.filter(market_cap__gte=min_cap)

        serializer = CryptoSerializer(queryset, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, name='price_points')
    def price_points(self, request, name=None):
        data = request.data
        try:
            crypto = Crypto.objects.get(name=name)
        except:
            return Response({"error": f"no coin with name {name}"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            points = CrytoPricePoint.objects.filter(crypto=crypto)[30*(data["page"]-1):30*(data["page"])]
            if len(points) < 20:
                raise Exception()
        except:
            return Response({"error": "error"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CryptoPricePointSerializer(points, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, name='filter_cryptos')
    def filter_cryptos(self, request):
        data: dict = request.data
        name = data.get("name", None)
        min_price = data.get("min_price", None)
        max_price = data.get("max_price", None)
        min_cap = data.get("min_cap", None)
        max_cap = data.get("max_cap", None)

        queryset = self.queryset
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
        


class NewsPagination(pagination.PageNumberPagination):
    page_size = 2


class CryptoNewsViewSet(viewsets.ModelViewSet):
    queryset = CryptoNews.objects.all()
    serializer_class = CryptoNewsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = NewsPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


