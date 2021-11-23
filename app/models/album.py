from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class Album(models.Model):
    """Model representing a album."""
    title = models.CharField(max_length=200,)
    release_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("album-detail", kwargs={"pk": self.pk})
