from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import (
    SignUpSerializer,
    UserConfirmationSerializer,
    UserForAdminSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserForAdminSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=self.request.user.email)

        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    if username == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.username = username
            user.save()
            if not request.user.is_anonymous and not request.user.is_admin:
                mail_subject = 'Код подтверждения на Yamdb.ru'
                message = f'Ваш код подтверждения: {user.confirmation_code}'
                send_mail(mail_subject, message, settings.EMAIL_FROM, [email])
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = UserConfirmationSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if user and str(user.confirmation_code) == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Invalid confirmation code'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
