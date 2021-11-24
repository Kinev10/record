from rest_framework import fields, serializers

import app.models as models
from app.models import band
from .album import AlbumSerializer
from .member import MemberSerializer

import datetime

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
                            w = models.Artist.objects.get(id=writer["id"])
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
                    a = models.Artist.objects.get(id=artist["id"])
                else:
                    continue
            else:
                a = models.Artist.objects.create(**artist)
            # will catch by unique_together constraint
            member = models.Member.objects.create(artist=a, band=band, **member)
            member.join_date = datetime.date.today()
            member.save()
            
        return band

    def update(self, instance, validated_data):
        albums = validated_data.pop("albums")
        members = validated_data.pop("members")

        instance.name = validated_data.get("name", instance.name)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()

        # consider deleted or modified albums
        keep_albums = []
        for album in albums:
            # consider deleted or modified songs
            songs = album.pop("songs")
            if "id" in album.keys():
                # modify album
                if models.Album.objects.filter(id=album["id"]).exists():
                    a = models.Album.objects.get(id=album["id"])
                    a.title = album.get("title", a.title)
                    a.release_date = album.get("release_date", a.release_date)
                    a.save()
                    keep_albums.append(a.id)
                    keep_songs = []
                    for song in songs:
                        writers = song.pop("writers")
                        if "id" in song.keys():
                            # modify song
                            if models.Song.objects.filter(id=song["id"]).exists():
                                s = models.Song.objects.get(id=song["id"])
                                s.title = song.get("title", s.title)
                                s.duration = song.get("duration", s.duration)
                                s.save()
                                keep_songs.append(s.id)

                                # check if there's changes in song writers
                                keep_writers = []
                                for writer in writers:
                                    if "id" in writer.keys():
                                        if models.Artist.objects.filter(id=writer["id"]).exists():
                                            w = models.Artist.objects.get(id=writer["id"])
                                            w.name = writer.get("name", w.name)
                                            w.save()
                                            keep_writers.append(w.id)
                                        else:
                                            continue
                                    else:
                                        w = models.Artist.objects.create(song=s, **writer)
                                        keep_writers.append(w.id)

                                for writer in s.writers.all():
                                    if writer.id not in keep_writers:
                                        s.writers.remove(writer)
                            else:
                                continue
                        else:
                            # add new song
                            s = models.Song.objects.create(album=a, **song)
                            keep_songs.append(s.id)
                            # consider that writer(artist) already exist
                            for writer in writers:
                                if "id" in writer.keys():
                                    if models.Artist.objects.filter(id=writer["id"]).exists():
                                        w = models.Artist.objects.get(id=writer["id"])
                                        s.writers.add(w)
                                    else:
                                        continue
                                else:
                                    s.writers.create(**writer)

                    for song in a.songs.all():
                        if song.id not in keep_songs:
                            song.delete()
                else:
                    continue
            else:
                # create new album
                a = models.Album.objects.create(band=instance, **album)
                keep_albums.append(a.id)

                for song in songs:
                    # all of the songs in the album is new
                    writers = song.pop("writers")
                    song = models.Song.objects.create(album=a, **song)
                    # consider that writer(artist) already exist
                    for writer in writers:
                        if "id" in writer.keys():
                            if models.Artist.objects.filter(id=writer["id"]).exists():
                                w = models.Artist.objects.get(id=writer["id"])
                                song.writers.add(w)
                            else:
                                continue
                        else:
                            song.writers.create(**writer)

        for album in instance.albums.all():
            if album.id not in keep_albums:
                album.delete()

        # get all bands existing members
        band_artists = list(instance.members.all().values_list('artist__id', flat=True))  
        keep_members = []
        for member in members:
            if "id" in member.keys():
                if models.Member.objects.filter(id=member["id"]).exists():
                    artist = member.pop("artist")
                    m = models.Member.objects.get(id=member["id"])
                    # check if new artist
                    if models.Artist.objects.filter(id=artist["id"]).exists():
                        a = models.Artist.objects.get(id=artist["id"])
                        # check swapped/changed artist
                        if a.id != m.artist.id and a.id in band_artists:
                            continue
                    else:
                        # new artist
                        a = models.Artist.objects.create(**artist)

                    print(artist)
                    # check if existing member
                    m.is_active = member.get("is_active", m.is_active)
                    m.role = member.get("role", m.role)
                    m.artist = a
                    m.save()
                    # add left date if the member is inactive
                    print(m.is_active)
                    if not m.is_active:
                        m.left_date = datetime.date.today()
                        m.save()
                    keep_members.append(m.id)
                else:
                    continue

            else:
                # add member
                artist = member.pop("artist")
                # consider that the artist already exist
                if "id" in artist.keys():
                    if models.Artist.objects.filter(id=artist["id"]).exists():
                        a = models.Artist.objects.get(id=artist["id"])
                        # check member: An artist cannot join a band after they leave it.
                        if a.id in band_artists:
                            continue
                    else:
                        continue
                else:
                    a = models.Artist.objects.create(**artist)
                # will catch by unique_together constraint
                m = models.Member.objects.create(artist=a, band=instance, **member)
                m.join_date = datetime.date.today()
                keep_members.append(m.id)

        for member in instance.members.all():
            if member.id not in keep_members:
                member.delete()
        return instance