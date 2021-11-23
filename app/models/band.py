from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class Band(models.Model):
    """Model representing a book."""
    name = models.CharField(max_length=200,)
    
    class Meta:
        verbose_name = _("Band")
        verbose_name_plural = _("Bands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("band-detail", kwargs={"pk": self.pk})
