from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
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

    def get_object(self):
        return self.queryset.objects.filter(row__dcid__id=self.kwargs['dcid'])

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
        return Rack.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # call the base implementaion to get a context
        context = super(RackView, self).get_context_data(**kwargs)
        # add all the assets
        #context['assets'] = Asset.objects.filter(rackid=self.rack)
        #context['height'] = [i+1 for i in range(self.rack.totalunits)]
        return context