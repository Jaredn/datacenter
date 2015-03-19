__author__ = 'jeff_dambly'

from django.forms import ModelForm
from django import forms
from racklayout.models import Asset, HalfUnit

class AssetForm(ModelForm):
    size = forms.IntegerField()
    topunit = forms.ModelChoiceField(queryset=HalfUnit.objects.all())


    class Meta:
        model = Asset