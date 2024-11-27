from django import forms
from .models import Waste

class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ['category', 'weight', 'date_collected', 'description']