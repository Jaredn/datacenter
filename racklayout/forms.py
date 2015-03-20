__author__ = 'jeff_dambly'

from django.forms import ModelForm
from django import forms
from racklayout.models import Asset, HalfUnit

UNITS = (('1','1'),)

class AssetForm(ModelForm):
    size = forms.IntegerField()
    rack = forms.IntegerField()


    def __init__(self, rack):
        self.rack = rack
        self.topunits = forms.ModelChoiceField(queryset=rack)
        super(AssetForm, self).__init__()

    class Meta:
        model = Asset
        fields = ['label', 'asset_type']