from django.forms import ModelForm

from models import User

class ContactForm(ModelForm):
    class Meta:
        model = User
        exclude = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
