from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (RegistrationSerializer,
                          LoginSerializer, ActivationSerializer,
                          ForgotPasswordSerializer,
                          ForgotPasswordCompleteSerializer, ChangePasswordSerializer)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Ваш аккаунт успешно зарегистрирован, на Вашу почту отправлено письмо '
                            'для подтверждения', status=201)
        return Response(serializer.errors, status=400)


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.activate()
            return Response('Пользователь успешно активирован')
        return Response(serializer.errors, status=400)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # разрешение на логаут может быть только у ЗАЛОГИНЕНОГО юзера

    def post(self, request):
        user = request
        Token.objects.filter(user=user).delete()
        return Response('Вы вышли с сайта')


"""создаёт код подтверждения на почту:"""
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_code()
            return Response('Вам выслан код для восстановления пароля')
        return Response(serializer.errors, status=400)


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.set_new_password()
            return Response('Пароль успешно обновлён')
        return Response(serializer.errors, status=400)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            serializer.set_new_password()
            return Response('Ваш пароль изменён')
        return Response(serializer.errors, status=400)