from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_active=False):
        if not email:
            raise ValueError(_("The email must be set."))

        user = self.model(username=email, email=email, is_active=is_active)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user
