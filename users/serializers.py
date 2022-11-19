from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, SmsCode


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('contract', 'phone')


class SmsCodeIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ('uuid',)


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ('uuid', 'code',)

    uuid = serializers.UUIDField()
