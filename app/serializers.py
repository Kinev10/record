from rest_framework import fields, serializers

from .models.album import Album
from .models.artist import Artist
from .models.band import Band
from .models.member import Member
from .models.song import Song

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ('id', 'name',)