__author__ = 'jeff_dambly'

from django.forms import ModelForm
from django import forms
from racklayout.models import Asset, HalfUnit

UNITS = (('1','1'),)

class AssetForm(ModelForm):
    size = forms.IntegerField()
    rack = forms.IntegerField()
    #topunit = forms.ChoiceField(choices=UNITS, required=True, label='Top Unit')

    class Meta:
        model = Asset
        fields = ['label', 'asset_type']