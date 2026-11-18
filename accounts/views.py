
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, ProfileSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='auth_profile_retrieve',
        responses={200: ProfileSerializer},
        description='Отримати профіль авторизованого користувача.',
    )
    def get(self, request):
        user = request.user

        return Response({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_staff': user.is_staff,
        })
