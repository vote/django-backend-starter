from django.contrib.auth import models as auth_models
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.enums import PoliticalParty
from common.fields import EnumField
from common.utils.models import TimestampModel, UUIDModel


class User(
    UUIDModel,
    TimestampModel,
    auth_models.AbstractBaseUser,
    auth_models.PermissionsMixin,
):
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_active = models.BooleanField(_("Active"), default=True)

    email = models.EmailField(_("Email Address"), editable=False, unique=True)

    political_party = EnumField(PoliticalParty, default=PoliticalParty.DEMOCRATIC)

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["created_at"]

    def __str__(self):
        return self.email
