__author__ = 'jeff_dambly'

from django.forms import ModelForm
from django import forms
from racklayout.models import Asset

class AssetForm(ModelForm):
    size = forms.IntegerField()

    class Meta:
        model = Asset