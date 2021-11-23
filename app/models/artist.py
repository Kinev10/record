from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class Artist(models.Model):
    """Model representing a artist."""
    name = models.CharField(max_length=200,)
    
    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("artist-detail", kwargs={"pk": self.pk})
