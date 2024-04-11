from django import forms


class CreateNewUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=50)
