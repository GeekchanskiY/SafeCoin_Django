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

    @action(methods=['post'], detail=False, name='change_password', serializer_class=UserSerializer)
    def change_password(self, request):
        data = request.data
        user: SCUser = request.user
        try:
            user.set_password(data["password"])
        except AttributeError:
            return Response({"detail": "no new password provided"}, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, name='change_country', serializer_class=UserSerializer)
    def change_country(self, request):
        data = request.data
        user: SCUser = request.user
        try:
            user.country = data["country"]
            user.save()
        except AttributeError:
            return Response({"detail": "no country provided"})
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, name='change_about_me', serializer_class=UserSerializer)
    def change_about_me(self, request):
        data = request.data
        user: SCUser = request.user
        try:
            user.about_me = data["about_me"]
            user.save()
        except AttributeError:
            return Response({"detail": "no about_me provided"})
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)





