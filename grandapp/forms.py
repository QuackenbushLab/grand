from django import forms

class ContactForm(forms.Form):
    contact_name    = forms.CharField(required=True, label="Name")
    contact_email   = forms.EmailField(required=True, label="Email")
    contact_subject = forms.CharField(required=True, label="Subject")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label="Message"
    )

class GeneForm(forms.Form):
    CHOICES = [('Targeted genes','Targeted genes'),('TF targeting','TF targeting')]
    contentup = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label="up"
    )
    contentdown = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label="down"
    )
    tfgene = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class DiseaseForm(forms.Form):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':20, 'cols':20}),
        label="disease"
    )

class DownloadForm(forms.Form):
    download_sample = forms.CharField(required=True, label="sample")
