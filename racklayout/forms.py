__author__ = 'jeff_dambly'

from django.forms import ModelForm
from django import forms
from racklayout.models import Asset, HalfUnit, Row

UNITS = (('1','1'),)

class AssetForm(ModelForm):
    size = forms.IntegerField()
    rack = forms.IntegerField()
    topunit = forms.ChoiceField(choices=UNITS, required=True, label='Top Unit')

    # def ___init__(self):
    #     super...
    #     self.fields['topunit'].choices = HalfUnit.objects.filter(rack=self.kwargs['pk'],
    #                                                       asset__isnull=True).order_by('-location')


    def __init__(self, rack):
        self.rack = rack
        self.topunits = forms.ModelChoiceField(queryset=rack)
        super(AssetForm, self).__init__()

    class Meta:
        model = Asset
        fields = ['label', 'asset_type']

class RowForm(ModelForm):
    class Meta:
        model = Row
        fields = ['dc', 'label']

    def clean_label(self):
        cleaned_data = self.cleaned_data
        cleaned_data['label'] = cleaned_data['label'].upper()
        return cleaned_data['label']
