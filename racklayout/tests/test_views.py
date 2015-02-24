from pprint import pprint
from django.http import HttpRequest
from django.test import TestCase
from racklayout.models import Metro, Dc, Rack, Row
from django.core.urlresolvers import resolve, Resolver404, reverse
from racklayout.views import CreateDc

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

    def test_createdc_url(self):
        found = resolve(reverse('racklayout:createdc'))
        self.assertEqual(found.url_name, 'createdc')
        self.assertEqual(found.func.func_name, 'CreateDc')

    def test_index_view(self):
        self.create_production_data()

        url = reverse('racklayout:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('datacenters' in response.context, 'Key datacenters not found in response.context' )
        self.assertEqual(response.context['datacenters'].count(), 30)

    def test_row_view(self):
        self.create_production_data()

        url = reverse('racklayout:dc', kwargs={'dcid':1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('row' in response.context, 'Key row not found in response.context')

    def test_rack_view(self):
        self.create_production_data()

        url = reverse('racklayout:rack', kwargs={'pk':1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        #keys = ('rack', 'asset', 'height')

        #for key in keys:
        #    self.assertTrue(key in response.context, 'Key: %s not found in response.context' % key)

    def test_createdc_view_can_save_a_post(self):
        metro = Metro.objects.create(label='ASH')

        request = HttpRequest()
        request.method = 'POST'
        request.POST['number'] = 1
        request.POST['metro'] = 1

        # todo figure out how this works with (request) doesn't make sense to me
        response = CreateDc.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dc.objects.all().count(), 1)

    def test_row_view_filters_queryset(self):
        self.create_production_data()

        url = reverse('racklayout:dc', kwargs={'dcid': 1})
        response = self.client.get(url)

        self.assertEqual(response.context['object_list'].count(), 10)

    def test_get_create_row(self):
        self.create_production_data()

        url = reverse('racklayout:createrow', kwargs={'pk': 1})
        response = self.client.get(url)
        print 'pk' in response.context
        pprint(response.context)
        pprint(response.context['form'])
        self.fail()