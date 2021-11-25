from django.test import TestCase

import app.models as models
import datetime
from django.db.models import Count, F, Q


class BandMemberTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        band = models.Band.objects.create(name='BLACKPINK')

        artist1 = models.Artist.objects.create(name='Lisa')
        artist2 = models.Artist.objects.create(name='Jennie')
        artist3 = models.Artist.objects.create(name='Jisoo')
        artist4 = models.Artist.objects.create(name='Rose')

        # 1 | left before 2010 | inactive
        band.members.create(artist=artist1, join_date=datetime.date(
            2009, 1, 3), left_date=datetime.date(2009, 12, 3), is_active=False, role='b')
        # 2 | joined after 2011 | active
        band.members.create(
            artist=artist2, join_date=datetime.date(2012, 1, 1), role='s')
        # 3 | left after 2011 | inactive
        band.members.create(artist=artist3, join_date=datetime.date(
            2009, 1, 3), left_date=datetime.date(2012, 1, 1), is_active=False, role='g')
        # 4 | joined today | active
        band.members.create(
            artist=artist4, join_date=datetime.date.today(), role='d')

    def test_active_members(self):
        band = models.Band.objects.get(id=1)
        active_members = band.members.filter(is_active=True)
        members = band.members.all()
        self.assertEqual(active_members.count(), 2)
        self.assertIn(members[1], active_members)
        self.assertIn(members[3], active_members)

    def test_band_formation(self):
        test_date = datetime.date(2010,1,1)
        band = models.Band.objects.get(id=1)
        filtered = band.members.filter(Q(Q(join_date__lte=test_date) & Q(is_active=True)) | Q(join_date__lte=test_date) & Q(left_date__gt=test_date))
        member3 = models.Member.objects.get(id=3)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(member3, filtered[0])
