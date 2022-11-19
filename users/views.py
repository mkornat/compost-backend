from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import SmsCode
from users.serializers import NewUserSerializer, SmsCodeIdSerializer, SmsCodeSerializer


class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=NewUserSerializer(),
        responses={
            201: SmsCodeIdSerializer()
        },
    )
    def post(self, request: Request) -> Response:
        new_user_serializer = NewUserSerializer(data=request.data)
        new_user_serializer.is_valid(raise_exception=True)
        new_user = new_user_serializer.save()

        sms_code = SmsCode()


class TokenObtainPairView(APIView):
    @swagger_auto_schema(
        request_body=SmsCodeSerializer(),
        responses={
            200: TokenRefreshSerializer(),
        }
    )
    def post(self, request: Request) -> Response:
        pass

