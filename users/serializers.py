from rest_framework import serializers

from users.models import SmsCode, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("contract", "phone")


class SmsCodeIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = ("uuid",)


class SmsCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmsCode
        fields = (
            "uuid",
            "code",
        )

    uuid = serializers.UUIDField()
