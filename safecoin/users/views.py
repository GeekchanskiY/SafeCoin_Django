from rest_framework import viewsets
from .serializers import UserSerializer
from .models import SCUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import FormParser, FileUploadParser
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = SCUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, FileUploadParser]


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'register':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(methods=['post'], detail=False, name='register', serializer_class=UserSerializer)
    def register(self, request):
        data = request.data

        test = SCUser.objects.filter(username=data["username"])
        if test:
            return Response({"error": "user with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        test = SCUser.objects.filter(username=data["email"])

        if test:
            return Response({"error": "user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = SCUser(
            username=data['username'],
            email=data['email'],
        )
        user.save()
        user.set_password(data["password"])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


            

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

    @action(methods=['post'], detail=False, name='change_avatar', serializer_class=UserSerializer)
    def change_avatar(self, request):
        user = request.user
        try:
            user.avatar = request.FILES['file']
            user.save()
            return Response({"detail": "avatar updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e.__str__()})





