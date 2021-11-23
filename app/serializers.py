from rest_framework import fields, serializers

from .models.album import Album
from .models.artist import Artist
from .models.band import Band
from .models.member import Member
from .models.song import Song





class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name',)


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ('id', 'name',)



class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('band', 'title','release_date',)



class SongSerializer(serializers.ModelSerializer):
    writers = ArtistSerializer(many=True)
    class Meta:
        model = Song
        fields = ('id','title', 'album', 'duration', 'writers')