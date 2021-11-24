from rest_framework import fields, serializers

from app.models.band import Band
from app.serializers.album_serializer import AlbumSerializer

class BandSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True)
    class Meta:
        model = Band
        fields = ('id', 'name', 'albums')
