from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import SmsCode, User
from users.serializers import SmsCodeIdSerializer, SmsCodeSerializer, UserSerializer


class SignInView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserSerializer(),
        responses={201: SmsCodeIdSerializer()},
    )
    def post(self, request: Request) -> Response:
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(phone=user_serializer.validated_data["phone"])
        except User.DoesNotExist:
            user = user_serializer.save()

        sms_code = SmsCode.objects.create(
            user=user,
        )

        # send SMS code here

        sms_code_id_serializer = SmsCodeIdSerializer(sms_code)
        return Response(data=sms_code_id_serializer.data, status=201)


class TokenObtainPairView(APIView):
    @swagger_auto_schema(
        request_body=SmsCodeSerializer(),
        responses={
            200: TokenRefreshSerializer(),
        },
    )
    def post(self, request: Request) -> Response:
        sms_code_serializer = SmsCodeSerializer(data=request.data)
        sms_code_serializer.is_valid(raise_exception=True)
        sms_code = get_object_or_404(SmsCode, uuid=sms_code_serializer.validated_data["uuid"])

        if settings.DEMO_SEND_SMS:
            valid = sms_code.code == sms_code_serializer.validated_data["code"]
        else:
            valid = settings.DEMO_STATIC_CODE == sms_code_serializer.validated_data["code"]
        if not valid:
            raise ValidationError("Invalid code")

        user = sms_code.user

        user.is_active = True
        user.save()

        token: RefreshToken = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(token),
                "access": str(token.access_token),
            }
        )
