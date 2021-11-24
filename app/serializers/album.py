from rest_framework import  serializers
from app.models.album import Album
from .song import SongSerializer

class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    songs = SongSerializer(many = True)
    class Meta:
        model = Album
        fields = ('id', 'band', 'title','release_date','songs')
        read_only_fields = ("band",)