from django.forms import ModelForm
from django import forms

from .models import Place

class PlaceForm(ModelForm):
    class Meta:
        model = Place
        exclude = ('map_web_url', )

    def save(self, commit=True, owner=None):
        if not self.instance.pk:
            if not owner:
                raise TypeError("Owner is required to create a Place.")
            self.instance.owner = owner
        return super(PlaceForm, self).save(commit)
