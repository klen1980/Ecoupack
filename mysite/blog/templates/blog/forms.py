from django import forms


class EmailPosrForm(forms.Form):
    name = forms.CharField(max_lengh=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget = forms.TextArea)