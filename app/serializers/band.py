from rest_framework import fields, serializers

from app.models.band import Band
from .album import AlbumSerializer
from .member import MemberSerializer

class BandSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True)
    members = MemberSerializer(many=True)
    class Meta:
        model = Band
        fields = ('id', 'name', 'albums', 'members')
