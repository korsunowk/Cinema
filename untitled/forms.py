from django import forms
from kinouser.models import Kinouser
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'required': 'required',
                                                            'class': "inp1 blue", 'style': "text-align:center"}))
    firstname = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'required': 'required',
                                                              'class': "inp2 green", 'style': "text-align:center"}))
    lastname = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'required': 'required',
                                                             'class': "inp1 red", 'style': "text-align:center"}))

    class Meta:
        model = Kinouser
        fields = ("email", 'firstname', 'lastname', "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
