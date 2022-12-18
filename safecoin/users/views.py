from rest_framework import viewsets
from .serializers import UserSerializer
from .models import SCUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = SCUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False, name='search', serializer_class=UserSerializer)
    def search(self, request):
        data = request.data.get('search', None)
        if data is not None:
            serializer = UserSerializer(list(self.queryset.filter(Q(username__contains=data))),
                                        many=True)

            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(list(self.queryset), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['get', 'options'], detail=False, name='me', serializer_class=UserSerializer)
    def me(self, request):
        data = request.user
        serializer = UserSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)



