from rest_framework import fields, serializers

from app.models.song import Song
from app.serializers.artist_serializer import ArtistSerializer

class SongSerializer(serializers.ModelSerializer):
    writers = ArtistSerializer(many=True)
    class Meta:
        model = Song
        fields = ('id','title', 'album', 'duration', 'writers')