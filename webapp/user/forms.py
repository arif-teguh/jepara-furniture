from django import forms

class RegisterUserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField() 
    password = forms.CharField()