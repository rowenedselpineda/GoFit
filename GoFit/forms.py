from django import forms
from .models import FitnessClass


class FitnessClassForm(forms.ModelForm):
    class Meta:
        model = FitnessClass
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)