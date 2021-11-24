from rest_framework import fields, serializers

import app.models as models
from .album import AlbumSerializer
from .member import MemberSerializer

class BandSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True)
    members = MemberSerializer(many=True)
    class Meta:
        model = models.Band
        fields = ('id', 'name', 'is_active', 'albums', 'members')

    def create(self, validated_data):
        albums = validated_data.pop("albums")        
        members = validated_data.pop("members")

        band = models.Band.objects.create(**validated_data)
        for album in albums:
            songs = album.pop("songs")
            album = models.Album.objects.create(band=band, **album)
            for song in songs:
                writers = song.pop("writers")
                song = models.Song.objects.create(album=album, **song)
                # consider that writer(artist) already exist
                for writer in writers:
                    if "id" in writer.keys():
                        if models.Artist.objects.filter(id=writer["id"]).exists():
                            w = models.Artist.objects.get(writer["id"])
                            song.writers.add(w)
                        else:
                            continue
                    else:
                        song.writers.create(**writer)

            for member in members:
                artist = member.pop("artist")
                # consider that the artist already exist
                if "id" in artist.keys():
                    if models.Artist.objects.filter(id=artist["id"]).exists():
                        a = models.Artist.objects.get(artist["id"])
                    else:
                        continue
                else:
                    a = models.Artist.objects.create(**artist)
                member = models.Member.objects.create(artist=a, band=band, **member)
                
        return band