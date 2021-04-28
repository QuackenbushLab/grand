from django import forms
from .models import Lala, netmod, tarmod, cluemod

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
    combin = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    ngenes = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '150', 'value':'100','id':'myRange'}), required=False
    )

class DiseaseForm(forms.Form):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':14, 'cols':20}),
        label="disease"
    )

class NetForm(forms.ModelForm):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES2  = [('no',''),('dtt',''),('dee',''),('bc','')]
    CHOICES3  = [('nosel',''),('by gene',''),('by tf',''),('by GO',''),('by GWAS','')]
    dt        = forms.ChoiceField(choices=CHOICES2, widget=forms.RadioSelect)
    topbottom = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    brd       = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    nosel     = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    absval    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    edgetargeting    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    tfgenesel = forms.ChoiceField(choices=CHOICES3, widget=forms.RadioSelect)
    nedges = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '150', 'value':'100','id':'myEdge'}), required=False
    )
    geneform = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':3, 'cols':7}),
        label="gene"
    )
    tfform = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':3, 'cols':7}),
        label="tf"
    )
    goform = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':1, 'cols':7}),
        label="go"
    )
    gwasform = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':1, 'cols':7}),
        label="gwas"
    )
    class Meta:
        model = netmod
        fields = '__all__'

class TarForm(forms.ModelForm):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES3  = [('nosel',''),('by gene',''),('by GO',''),('by GWAS','')]
    absvaltar    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    tfgeneseltar = forms.ChoiceField(choices=CHOICES3, widget=forms.RadioSelect)
    topbottomtar = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    nedgestar = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '150', 'value':'100','id':'myEdgeTar'}), required=False
    )
    absvaltartf    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    topbottomtartf = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    nedgestartf = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '150', 'value':'100','id':'myEdgeTartf'}), required=False
    )
    geneformtar = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':3, 'cols':7}),
        label="genetar"
    )
    goformtar = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':1, 'cols':7}),
        label="gotar"
    )
    gwasformtar = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows':1, 'cols':7}),
        label="gwastar"
    )
    class Meta:
        model = tarmod
        fields = '__all__'

class BabelForm(forms.ModelForm):
    CHOICES = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES2 = [('Histone','Histone'),('CNV','CNV'),('Methylation','Methylation'),('miRNA','miRNA'),('mRNA','mRNA'),('Protein','Protein'),('Metabolism','Metabolism'),('Drugs','Drugs'),('Dependency','Dependency')]
    topbottom = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    connex    = forms.ChoiceField(choices=CHOICES2, widget=forms.Select)
    cnv       = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    methyl    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    mir       = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    hm        = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    dep       = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    exp       = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    prot      = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    agg       = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    absval    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    gp        = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    allay     = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    nedges = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '150','id':'myEdge2'}), required=False
    )
    class Meta:
        model = Lala
        fields = '__all__'

class ClueForm(forms.ModelForm):
    CHOICES3  = [('by gene',''),('by tf','')]
    tfgeneselclue = forms.ChoiceField(choices=CHOICES3, widget=forms.RadioSelect)
    class Meta:
        model = cluemod
        fields = '__all__'

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )