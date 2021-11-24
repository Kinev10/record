from rest_framework import  serializers

from app.models.artist import Artist

class ArtistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Artist
        fields = ('id', 'name',)