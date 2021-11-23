from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class BandActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Band(models.Model):
    """Model representing a book."""
    name = models.CharField(max_length=200,)
    is_active = models.BooleanField(_("Is Active"), default=True)

    objects = models.Manager()
    active = BandActiveManager()
    
    class Meta:
        verbose_name = _("Band")
        verbose_name_plural = _("Bands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("band-detail", kwargs={"pk": self.pk})
