from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
#### app imports
from racklayout.forms import AssetForm
from racklayout.models import Dc, Rack, Asset, Row, HalfUnit

# Create your views here.

class IndexView(ListView):
    """
    simple view for my index page
    """
    model = Dc
    template_name = 'racklayout/index.html'
    context_object_name = 'datacenters'

class RowView(ListView):
    """
    view for the all the rows in a datacenter
    Note: must use object_list in the template only way I could get it to work :/
    """
    model = Row
    template_name = 'racklayout/row.html'
    context_object_name = 'row'

    #def get_object(self):
    #    return self.queryset.objects.filter(row__dc__dc_id=self.kwargs['dcid'])
    def get_queryset(self):
        return Row.objects.filter(dc_id=self.kwargs['dcid'])

    def get_context_data(self, **kwargs):
        context = super(RowView, self).get_context_data(**kwargs)
        context['datacenter'] = Dc.objects.get(id=self.kwargs['dcid'])

        return context

class RackView(DetailView):
    """
    view for the racks

    """
    model = Rack
    template_name = 'racklayout/new_rack.html'
    context_object_name = 'rack'

    def get_queryset(self):
        self.rack = get_object_or_404(Rack, pk=self.kwargs['pk'])
        return self.model.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # call the base implementaion to get a context
        context = super(RackView, self).get_context_data(**kwargs)
        # add all the assets
        context['assets'] = Asset.objects.filter(rack=self.rack)
        context['totalunits'] = range(1, self.rack.totalunits+1)[::-1]

        assets =  context['assets']
        totalunits = context['totalunits']
        # create a dict that can used in the template to render the rack

        # Query the HalfUnits instead of the Assets: HalfUnit.objects.filter(rack=self.rack).order_by('-label')
        # and then in the template skip emitting a <td> if the asset.id is the same as in the row above
        context['backunits'] = self._format_rack(assets, totalunits, 1)[::-1]
        context['frontunits'] = self._format_rack(assets, totalunits, 0)[::-1]

        return context

    def _format_rack(self, assets, totalunits, part):
        """
        method to massage the data into something that used by the template to render the rack
        example output
        [{48: {'type': '', 'label': 'empty'}}, {47: {'type': '', 'label': 'empty'}},
        {46: {'size': 2, 'type': u'network', 'label': <Asset: lsw1.lab>}} }]

        template needs to see label is fill, empty or has an asset

        :param assets:
        :param totalunits:
        :param part: 0 -> front, 1 -> back
        :return: list of dicts
        """
        result = {}
        listresult = []

        for unit in totalunits:
            result.update({unit: {'type': '', 'label': 'empty'}})

        # populate the assets into the result dict
        for asset in assets:
            key = asset.units.first().location

            if asset.units.first().part == part:
                result[key]['label'] = asset
                result[key]['type'] = asset.get_asset_type_display()
                result[key]['size'] = asset.units.all().count()

            for unit in asset.units.filter(part=part)[1:]:
                result[unit.location]['type'] = 'filled'
                result[unit.location]['label'] = 'filled'

        for each in result:
            listresult.append({each: result[each]})

        return listresult

class CreateDc(CreateView):

    model = Dc
    fields = ['metro', 'number']
    success_url = "/racklayout/"


class CreateRow(CreateView):
    model = Row
    fields = ['dc', 'label']

    def get_initial(self):
        intial = super(CreateRow, self).get_initial()
        intial['dc'] = get_object_or_404(Dc, pk=self.kwargs['pk'])
        return intial

    def get_form(self, form_class):
        form = super(CreateRow, self).get_form(form_class)
        datacenter = get_object_or_404(Dc, pk=self.kwargs['pk'])
        form.fields['dc'].queryset = Dc.objects.filter(pk=datacenter.id)
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateRow, self).get_context_data(**kwargs)
        context['datacenter'] = self.kwargs['pk']

        return context

class CreateRack(CreateView):
    model = Rack
    fields = ['row', 'label', 'totalunits']

    def get_form(self, form_class):
        form = super(CreateRack, self).get_form(form_class)
        datacenter = get_object_or_404(Dc, pk=self.kwargs['pk'])
        form.fields['row'].queryset = Row.objects.filter(dc=datacenter)
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateRack, self).get_context_data(**kwargs)
        context['datacenter'] = self.kwargs['pk']

        return context

class CreateAsset(CreateView):
    model = Asset
    form_class = AssetForm
    fields = ['label', 'asset_type']

    def get_context_data(self, **kwargs):
        context = super(CreateAsset, self).get_context_data(**kwargs)
        context['rack'] = self.kwargs['pk']

        return context

    def get_form(self, form_class):
        form = super(CreateAsset, self).get_form(form_class)
        # form['topunit'].choices = self._get_empty_rack_units(0)
        form['topunit'].choices = HalfUnit.objects.filter(rack=self.kwargs['pk'], asset__isnull=True).order_by('-location')

        return form

    def _get_empty_rack_units(self, part):

        rack = get_object_or_404(Rack, pk=self.kwargs['pk'])
        result = []

        totalunits = range(1, rack.totalunits+1)[::1]

        for unit in totalunits:
            result.append((unit,unit))

        assets = Asset.objects.filter(rack=rack)

        if not assets:
            return result
        else:
            for asset in assets:
                index = asset.units.first().location
                result.remove((index,index))

                for unit in asset.units.filter(part=part)[1:]:
                    result.remove((unit.location, unit.location))

        return result
