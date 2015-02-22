__author__ = "Jeff d'Ambly"

from django.test import TestCase

from racklayout.models import Metro, Dc, Row, Rack, Asset


# todo: Metro creation is copy pasta - duplicate code

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

        asset = Asset()
        asset.label = 'trr1-10f.lab.net'
        asset.asset_type = asset.ASSET_TYPES[2]
