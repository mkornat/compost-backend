import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phone_field import PhoneField


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'phone'

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True
    )
    phone = PhoneField(
        null=False,
        blank=False,
        unique=True
    )


class SmsCode(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=5)
