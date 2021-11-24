from rest_framework import fields, serializers

from app.models.song import Song
from .artist import ArtistSerializer

class SongSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    writers = ArtistSerializer(many=True)
    class Meta:
        model = Song
        fields = ('id', 'album', 'title',  'duration', 'writers')
        read_only_fields = ("album",)
