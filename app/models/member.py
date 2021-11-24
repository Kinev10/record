from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class Member(models.Model):
    """Model representing a band member connection to artist."""
    ROLE_CHOICES = (
        ('s', 'Lead Singer'),
        ('g', 'Lead Guitar'),
        ('b', 'Bass'),
        ('d', 'Drums'),
    )
    band = models.ForeignKey("app.Band", verbose_name=_("Band"), on_delete=models.CASCADE, related_name="members")
    artist = models.ForeignKey("app.Artist", verbose_name=_("Artist"), on_delete=models.CASCADE, related_name="members")
    join_date = models.DateField(_("Date Joined"), auto_now=False, auto_now_add=False)
    left_date = models.DateField(_("Date Left"), auto_now=False, auto_now_add=False, null=True, blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
    )

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")
        unique_together = ('band', 'artist',)

    def __str__(self):
        return f'{self.band} -{self.artist} - {self.get_role_display()}'

    def get_absolute_url(self):
        return reverse("album-detail", kwargs={"pk": self.pk})
