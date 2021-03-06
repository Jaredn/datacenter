from pprint import pprint
from django.core.exceptions import ValidationError

__author__ = "Jeff d'Ambly"

from django.test import TestCase

from racklayout.models import Metro, Dc, Row, Rack, Asset, HalfUnit


# todo: Metro creation is copy pasta - duplicate code - use objects.create to fix this

# model tests
class TestAllTheModels(TestCase):

    def test_metro_model_insert(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        self.assertTrue(isinstance(metro, Metro))
        self.assertEqual(metro.__unicode__(), metro.label)

    def test_metro_regex(self):
        metro = Metro()
        metro.lab = 'a12'

        self.assertRaises(ValidationError, metro.full_clean)
        self.assertEqual(metro.save(), None)


    def test_dc_model_insert(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        dc = Dc()
        dc.number = 1
        dc.metro = metro
        dc.save()

        self.assertTrue(isinstance(dc, Dc))
        self.assertEqual(dc.__unicode__(), '%s%d' % (dc.metro.label, dc.number))

    def test_row_model_insert_number(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        dc = Dc()
        dc.number = 1
        dc.metro = metro
        dc.save()

        row = Row()
        row.label = 1
        row.dc = dc
        row.save()

        self.assertTrue(isinstance(dc, Dc))
        self.assertEqual(row.__unicode__(), '%s' % row.label)

    def test_row_model_insert_letter(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        dc = Dc()
        dc.number = 1
        dc.metro = metro
        dc.save()

        row = Row()
        row.label = "A"
        row.dc = dc
        row.save()

        self.assertTrue(isinstance(dc, Dc))
        self.assertEqual(row.__unicode__(), '%s' % row.label)

    def test_row_model_insert_test_regex(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        dc = Dc()
        dc.number = 1
        dc.metro = metro
        dc.save()
        dc = Dc.objects.get(number=1)

        row = Row()
        row.label = "a"
        row.dc = dc

        self.assertEqual(row.save(), None)

        row.label = 'A11'

        self.assertEqual(row.save(), None)

    def test_rack_model_insert(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        dc = Dc()
        dc.number = 1
        dc.metro = metro
        dc.save()

        row = Row()
        row.label = 10
        row.dc = dc
        row.save()

        rack = Rack()
        rack.label = 'A'
        rack.row = row
        # total units should default to 48
        rack.save()

        self.assertTrue(isinstance(rack, Rack))
        self.assertEqual(rack.__unicode__(), '%s%s' % (row.label, rack.label))
        self.assertEqual(rack.totalunits, 48)

    def test_asset_model_insert(self):
        metro = Metro()
        metro.label = 'ASH'
        metro.save()

        dc = Dc()
        dc.number = 1
        dc.metro = metro
        dc.save()

        row = Row()
        row.label = 10
        row.dc = dc
        row.save()

        rack = Rack()
        rack.label = 'A'
        rack.row = row
        # total units should default to 48
        rack.save()

        asset = Asset.objects.create(label='trr1-10f.lab.net',
                     asset_type=2)

        self.assertTrue(isinstance(asset, Asset))
        self.assertEqual(asset.__unicode__(), 'trr1-10f.lab.net')
        #self.assertNotEqual(asset.save(), None)

    def test_halfunit_model_insert(self):
        metro = Metro.objects.create(label='ASH')
        dc = Dc.objects.create(number=1, metro=metro)
        row = Row.objects.create(label=1, dc=dc)
        rack = Rack.objects.create(label='A', row=row)
        asset = Asset.objects.create(label='trr1-10f.lab.net', asset_type=2)
        front_unit = HalfUnit.objects.create(part=0, asset=asset, location=48)

        self.assertTrue(isinstance(front_unit, HalfUnit))
        self.assertEqual(front_unit.__unicode__(), '%s, %s, %s' % (asset, 48, 'front') )

# todo have to check to make sure we have the same row and rack labels in mutiple dataceters

    def test_insert_the_same_row_in_two_datacenters(self):
        """
        for some reason objects.create doesn't for some reason doesn't seem
        to be using our validation :/ have to do this with .full_clean() and then save
        perhaps this the start of a custom manager?

        """
        metro = Metro.objects.create(label='ASH')
        dc1 = Dc.objects.create(number=1, metro=metro)
        dc2 = Dc.objects.create(number=2, metro=metro)
        dc1row1 = Row(label='A', dc=dc1)
        dc1row1.full_clean()
        dc1row1.save()
        dc2row1 = Row(label='A', dc=dc2)
        dc2row1.full_clean()
        dc2row1.save()

        self.assertTrue(isinstance(metro, Metro))
        self.assertTrue(isinstance(dc1, Dc))
        self.assertTrue(isinstance(dc2, Dc))
        self.assertTrue(isinstance(dc1row1, Row))
        self.assertTrue(isinstance(dc2row1, Row))

    def test_insert_two_of_the_same_rows_in_the_same_dc(self):
        metro = Metro.objects.create(label='ASH')
        dc1 = Dc.objects.create(number=1, metro=metro)

        dc1row1 = Row(label='A', dc=dc1)
        dc1row1.full_clean()
        dc1row1.save()
        dc2row1 = Row(label='A', dc=dc1)

        self.assertRaises(ValidationError, dc2row1.full_clean)

    def test_insert_two_of_the_same_rack_in_the_same_row(self):

        metro = Metro.objects.create(label='ASH')
        dc = Dc.objects.create(number=1, metro=metro)
        row = Row.objects.create(label='A', dc=dc)
        rack1 = Rack(label=1, row=row)
        rack1.full_clean()
        rack1.save()

        rack2 = Rack(label=1, row=row)
        self.assertRaises(ValidationError, rack2.full_clean())

    def test_insert_two_of_the_same_assset_in_the_same_unit(self):
        metro = Metro.objects.create(label='ASH')
        dc = Dc.objects.create(number=1, metro=metro)
        row = Row.objects.create(label='A', dc=dc)
        rack = Rack.objects.create(label='1', row=row)
        asset = Asset.objects.create(label='trr1-10f.lab.net', asset_type=2, rack=rack)
        front_unit1 = HalfUnit.objects.create(part=0, location=48, asset=asset)

        front_unit2 = HalfUnit(part=0, location=48, asset=asset)

        self.assertRaises(ValidationError, front_unit2.full_clean)

    def create_production_data(self):
        metro1 = Metro.objects.create(label='ASH')
        metro2 = Metro.objects.create(label='PHX')
        metro3 = Metro.objects.create(label='SJC')

        metros = (metro1, metro2, metro3)

        for metro in metros:
            for i in xrange(10):
                number = int(i)+1
                dc = Dc(number=number, metro=metro)
                dc.full_clean()
                dc.save()

        for dc in Dc.objects.all():
            for i in 'ABCDEFGHIJ':
                row = Row(label=i, dc=dc)
                row.full_clean()
                row.save()

        for row in Row.objects.all():
            for i in xrange(10):
                label = int(i)
                rack = Rack(label=label, row=row)
                rack.full_clean()
                rack.save()

    def test_production(self):
        self.create_production_data()

        self.assertEqual(Dc.objects.all().count(), 30)
        self.assertEqual(Row.objects.all().count(), 300)
        self.assertEqual(Rack.objects.all().count(), 3000)

        rows = Row.objects.filter(dc__number=1, dc__metro__label='ASH')
        for row in rows:
            self.assertEqual(row.racks.count(), 10)


