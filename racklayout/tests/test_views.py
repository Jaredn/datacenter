from pprint import pprint
from django.test import TestCase
from racklayout.models import Metro, Dc, Rack, Row
from django.core.urlresolvers import resolve, Resolver404, reverse
from racklayout.views import IndexView

class TestIndexView(TestCase):

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

    def test_root_url_does_not_resolve(self):
        self.assertRaises(Resolver404, resolve, '/')

    def test_admin_url(self):
        found = resolve('/admin/')
        self.assertEqual(found.app_name, 'admin')

    def test_racklayout_url(self):
        found = resolve('/racklayout/')
        self.assertEqual(found.namespace, 'racklayout')

    def test_racklaout_index_url(self):
        found = resolve(reverse('racklayout:index'))
        self.assertEqual(found.url_name, 'index')
        self.assertEqual(found.func.func_name, 'IndexView')

    def test_racklaout_rack_url(self):
        found = resolve(reverse('racklayout:rack', kwargs={'pk':1}))
        self.assertEqual(found.url_name, 'rack')
        self.assertEqual(found.func.func_name, 'RackView')

    def test_racklaout_dc_url(self):
        # todo might want to change the url to something else name is row kinda confusing
        found = resolve(reverse('racklayout:dc', kwargs={'dcid':1}))
        self.assertEqual(found.url_name, 'dc')
        self.assertEqual(found.func.func_name, 'RowView')