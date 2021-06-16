from django.db import models
from django.utils.translation import ugettext_lazy as _

from actnow.accounts.models import ActNowUser
from actnow.db.models import TimestampedModelMixin


class Petition(TimestampedModelMixin):
    title = models.CharField(
        _("title"),
        max_length=255,
    )
    description = models.CharField(
        _("details of petition"),
        max_length=1024,
        blank=True,
    )
    owner = models.ForeignKey(
        ActNowUser,
        on_delete=models.CASCADE,
    )
    recipients = models.CharField(
        _("recipients"),
        max_length=255,
    )
    problem_statement = models.CharField(
        _("problem statement"),
        max_length=1024,
    )
    number_of_signatures_required = models.PositiveIntegerField(
        _("number of signatures required")
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
        return self.title


class PetitionSignature(TimestampedModelMixin):
    petition = models.ForeignKey(
        Petition,
        on_delete=models.CASCADE,
    )
    signatory = models.ForeignKey(
        ActNowUser,
        on_delete=models.CASCADE,
    )
    comment = models.CharField(
        _("comment"),
        max_length=1024,
        blank=True,
    )

    def __str__(self):
        return "%s signed by %s" % (
            self.petition,
            self.signatory,
        )

    class Meta:
        unique_together = ("petition", "signatory")
