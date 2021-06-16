from django.db import models
from django.utils.translation import ugettext_lazy as _

from actnow.accounts.models import ActNowUser
from actnow.db.models import TimestampedModelMixin


class Petition(TimestampedModelMixin):
    title = models.CharField(
        _("title"),
        max_length=255,
    )
    description = models.TextField(_("details of petition"), blank=True)
    owner = models.ForeignKey(
        ActNowUser,
        on_delete=models.CASCADE,
    )
    recipients = models.CharField(
        _("recipients"),
        max_length=255,
    )
    problem_to_address = models.TextField(
        _("problem to be addressed"),
    )
    number_of_signature_required = models.IntegerField(
        _("number of signature required")
    )
    image = models.ImageField(
        _("image"),
        blank=True,
    )
    video = models.FileField(
        _("vide"),
        blank=True,
    )

    def __str__(self):
        return self.title


class PetitionSignature(TimestampedModelMixin):
    petition = models.ForeignKey(
        Petition,
        on_delete=models.CASCADE,
    )
    signator = models.ForeignKey(
        ActNowUser,
        on_delete=models.CASCADE,
        verbose_name="user who signed the petition",
    )
    comment = models.TextField(
        _("comment"),
        blank=True,
    )

    def __str__(self):
        return "%s signed by %s on %s" % (
            self.petition,
            self.signator,
            str(self.created_at),
        )

    class Meta:
        unique_together = ("petition", "signator")
