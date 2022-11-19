from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone: str, **extra_fields):
        if not phone:
            raise ValueError("Phone must be set")
