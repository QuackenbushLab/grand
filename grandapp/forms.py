from django import forms

class ContactForm(forms.Form):
    contact_name    = forms.CharField(required=True, label="Name")
    contact_email   = forms.EmailField(required=True, label="Email")
    contact_subject = forms.CharField(required=True, label="Subject")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':7, 'cols':20}),
        label="Message"
    )

class GeneForm(forms.Form):
    CHOICES = [('Gene targeting','Gene targeting'),('TF targeting','TF targeting')]
    contentup = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':7, 'cols':20}),
        label="up"
    )
    contentdown = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':7, 'cols':20}),
        label="down"
    )
    tfgene = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    brd    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    ngenes = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '150', 'value':'100','id':'myRange'}), required=False
    )

class DiseaseForm(forms.Form):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':14, 'cols':20}),
        label="disease"
    )
