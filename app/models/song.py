from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

class Song(models.Model):
    """Model representing a song."""
    album = models.ForeignKey("app.Album", verbose_name=_("Album"), on_delete=models.CASCADE, related_name="songs", null=True)
    title = models.CharField(max_length=200,)
    duration = models.FloatField(_("Duration"))
    writer = models.ManyToManyField("app.Artist", verbose_name=_("Writer"))

    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("song-detail", kwargs={"pk": self.pk})
