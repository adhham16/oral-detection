from django import forms
from .models import Patients


class DetailsForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = "__all__"
