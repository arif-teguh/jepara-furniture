from django import forms

class RegisterUserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField() 
    password = forms.CharField()

class AddChairForm(forms.Form):
    nama = forms.CharField()
    harga = forms.IntegerField()