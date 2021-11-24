from rest_framework import fields, serializers

from app.models.member import Member
from .artist import ArtistSerializer

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    artist = ArtistSerializer()
    class Meta:
        model = Member
        fields = ('id','band','artist','join_date','left_date', 'is_active')
        read_only_fields = ("band",)

        