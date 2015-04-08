from django.forms import forms

from models import User


# class UploadForm(forms.Form):
#     filename = forms.CharField(label='File Name', max_length=100)
#     docfile = forms.FileField(
#         label='Selecciona un archivo'
#     )

class CreateMasivePropertiesForm(forms.Form):
    generate = forms.CharField(label='Your name', max_length=100)