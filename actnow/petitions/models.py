import hyperlink
from django.db import models
from django.utils.translation import ugettext_lazy as _

from actnow.db.models import TimestampedModelMixin
from actnow.profiles.models import Profile


class Petition(TimestampedModelMixin):
    title = models.CharField(
        _("title"),
        max_length=255,
    )
    description = models.TextField(
        _("details of petition"),
        max_length=1024,
    )
    owner = models.ForeignKey(
        Profile,
        verbose_name=_("owner"),
        on_delete=models.SET_NULL,
        null=True,
    )
    followers = models.ManyToManyField(
        Profile,
        verbose_name=_("followers"),
        related_name="petitions",
    )
    recipients = models.CharField(
        _("recipients"),
        max_length=255,
    )
    problem_statement = models.TextField(
        _("problem statement"),
        max_length=1024,
    )
    source = models.ForeignKey(
        "source",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    number_of_signatures_required = models.PositiveIntegerField(
        _("number of signatures required"),
        default=0,
    )
    image = models.ImageField(
        _("image"),
        blank=True,
    )
    video = models.FileField(
        _("video"),
        blank=True,
    )

    def __str__(self):
        return f"{self.title} by {self.owner}"


class Signature(TimestampedModelMixin):
    petition = models.ForeignKey(
        Petition,
        related_name="signatures",
        on_delete=models.CASCADE,
        verbose_name=_("petition"),
    )
    signatory = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        verbose_name=_("signatory"),
        null=True,
    )
    comment = models.CharField(
        _("comment"),
        max_length=255,
        blank=True,
    )
    anonymous = models.BooleanField(verbose_name=_("anonymous"), default=False)

    def __str__(self):
        return f"{self.petition} signed by {self.signatory}"

    class Meta:
        unique_together = ("petition", "signatory")


class Source(TimestampedModelMixin):
    link = models.URLField(_("link"), unique=True)

    def __str__(self):
        return self.link

    def clean(self):
        self.link = hyperlink.URL.from_text(self.link).normalize().to_text()
        return super().clean()
