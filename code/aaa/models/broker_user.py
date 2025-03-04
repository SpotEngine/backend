from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.base_models import BaseModel
from django.core import validators
from django.utils.deconstruct import deconstructible
from .manager import UserManager


@deconstructible
class UnicodeEmailValidator(validators.RegexValidator):
    regex = r"^[\w.@]+\Z"
    message = _(
        "Enter a valid email. This value may contain only letters, "
        "numbers, and @/. characters."
    )
    flags = 0


class BrokerUser(AbstractUser, BaseModel):
    email_validator = UnicodeEmailValidator()

    email = models.EmailField(
        _("email address"), 
        unique=True,
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/. only."
        ),
        validators=[email_validator],
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

