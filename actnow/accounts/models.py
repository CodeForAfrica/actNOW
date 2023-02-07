import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from oauth2_provider.models import (
    AbstractAccessToken,
    AbstractApplication,
    AbstractGrant,
    AbstractIDToken,
    AbstractRefreshToken,
)

from actnow.db.models import TimestampedModelMixin


class ActNowUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        username = extra_fields.get("username", "").strip()
        # Ensure we have a username
        if not username:
            username = uuid.uuid4().hex

        is_staff = extra_fields.pop("is_staff")
        is_active = extra_fields.pop("is_active")
        is_superuser = extra_fields.pop("is_superuser")
        user = self.model(
            email=email,
            username=username,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.set_password(password)

        # Pass on username
        extra_fields["username"] = username
        user.extra_fields = extra_fields
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # is_staff is required to login in order to complete OAuth.
        extra_fields["is_staff"] = True
        extra_fields["is_active"] = True
        extra_fields["is_superuser"] = False

        return self._create_user(email=email, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class ActNowUser(AbstractBaseUser, PermissionsMixin, TimestampedModelMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        # Required to work when unique=True, blank=True are set
        # https://docs.djangoproject.com/en/3.2/ref/models/fields/#null
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active. "),
    )
    is_deleted = models.BooleanField(
        _("deleted"),
        default=False,
        help_text=_("Designates whether this user should be treated as deleted."),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = ActNowUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class ActNowApplication(AbstractApplication):
    user = models.OneToOneField(ActNowUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Application"


# While we only need to override AccessToken and RefreshToken to increase
# token field length to support JWT, there are a lot of issues around
# swapping DOT models and the most recommended solutions appear to just
# override all
# see: https://github.com/jazzband/django-oauth-toolkit/issues/634


class Grant(AbstractGrant):
    application = models.ForeignKey(
        ActNowApplication,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class AccessToken(AbstractAccessToken):
    source_refresh_token = models.OneToOneField(
        # unique=True implied by the OneToOneField
        "RefreshToken",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="refreshed_access_token",
    )
    token = models.CharField(
        max_length=2048,
        unique=True,
    )
    id_token = models.OneToOneField(
        "IDToken",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="access_token",
    )
    application = models.ForeignKey(
        ActNowApplication,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class RefreshToken(AbstractRefreshToken):
    token = models.CharField(
        max_length=2048,
        unique=True,
    )
    application = models.ForeignKey(
        ActNowApplication,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    access_token = models.OneToOneField(
        "AccessToken",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="refresh_token",
    )


class IDToken(AbstractIDToken):
    application = models.ForeignKey(
        ActNowApplication,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
