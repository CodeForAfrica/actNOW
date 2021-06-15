 
from django.db import models
from django.contrib.auth.models import User

from actnow.db.models import TimestampedModelMixin

class Petition(TimestampedModelMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("details of petition"), blank=True)
    owner = models.ForeignKey(User, _("owner of petition"))
    recipients = models.CharField(_("recipients"), max_length=255)
    problem_to_address = models.TextField(_("problem to be addressed"))
    number_of_signature_required = models.IntegerField(_("number of signature required"))
    image = models.ImageField(_("image"), blank=True)
    video = models.FileField(_("vide"), blank=True)

    def __str__(self):
        return self.title

class PetitionSignature(TimestampedModelMixin):
    petition = models.ForeignKey(Petition, _("associated petition"))
    signator = models.ForeignKey(User, _("user who signed the petition"))
    comment = models.TextField(_"comments"), blank=True)

    def __str__(self):
        return '%s signed by %s on %s' % (self.petition, self.signator, str(self.created_at))

    class Meta:
        unique_together = ("petition", "signator")
