from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View
from django.shortcuts import get_object_or_404
#### app imports
from racklayout.models import Dc, Rack, Asset, Row

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
    template_name = 'racklayout/rack.html'
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
        listresult = []
        result = {}
        for unit in totalunits:
            result.update({unit: {'type': '', 'label': 'empty'}})

        # populate the assets into the result dict
        for asset in assets:
            key = asset.units.first().location
            result[key]['label'] = asset
            result[key]['type'] = asset.get_asset_type_display()
            result[key]['size'] = asset.units.all().count()
            for unit in asset.units.all()[1:]:
                result[unit.location]['type'] = 'filled'
                result[unit.location]['label'] = 'filled'

        for each in result:
            listresult.append({each: result[each]})

        context['rackunits'] = result
        context['listunits'] = listresult[::-1]

        return context


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