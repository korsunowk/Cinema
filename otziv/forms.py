from django import forms

class OtzivForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    text = forms.Textarea()
    date = forms.DateField(required=False)
