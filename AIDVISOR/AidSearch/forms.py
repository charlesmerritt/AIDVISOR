from django import forms


class CreateNewUserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=200, widget=forms.TextInput(attrs={'class': 'forms'}))
    password = forms.CharField(label="Password", max_length=300, widget=forms.TextInput(attrs={'class': 'forms'}))
