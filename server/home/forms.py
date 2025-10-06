from django import forms
from utility.models import ContactUs


class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "cs_form_field"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "cs_form_field"}),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "cs_form_field"}),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)

    def save(self):
        data = self.cleaned_data
        submission = ContactUs.objects.create(**data)
        return submission


class SubscribeForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "cs_form_field"}),
    )