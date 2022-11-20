import random
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phone_field import PhoneField

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "phone"

    objects = UserManager()

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.CharField(max_length=255, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=15, null=False, blank=False, unique=True)
    password = models.CharField(max_length=128, null=False, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


def generate_sms_code() -> str:
    return random.choices(list(str(n) for n in range(10)), k=settings.SMS_CODE_LENGTH)


class SmsCode(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=settings.SMS_CODE_LENGTH, default=generate_sms_code)
