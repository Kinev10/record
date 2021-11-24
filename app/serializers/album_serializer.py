from rest_framework import fields, serializers

from app.models.album import Album
from app.serializers.song_serializer import SongSerializer

class AlbumSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many = True)
    class Meta:
        model = Album
        fields = ('band', 'title','release_date','songs')