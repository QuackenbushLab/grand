from django import forms
from .models import Lala, netmod, tarmod, cluemod, compmod, difftarmod

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
        required=False,
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
    geneform = forms.TextField(
        required=False,
        widget=forms.Textarea(attrs={'rows':3, 'cols':7, 'maxlength':100000}),
        label="gene",
        max_length=100000
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
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '250', 'value':'100','id':'myEdgeTar'}), required=False
    )
    absvaltartf    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    topbottomtartf = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    nedgestartf = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '250', 'value':'100','id':'myEdgeTartf'}), required=False
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
        help_text='max. 500 megabytes'
    )

class CompForm(forms.ModelForm):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES2  = [('no',''),('dtt',''),('bc','')]
    CHOICES3  = [('nosel',''),('by gene',''),('by tf',''),('by GO',''),('by GWAS','')]
    CHOICES4  = [('Adipose_Subcutaneous','Adipose Subcutaneous'),('Adipose_Visceral','Adipose Visceral'),('Adrenal_Gland','Adrenal Gland'),('Artery_Aorta','Artery Aorta'),('Artery_Coronary','Artery Coronary'),('Artery_Tibial','Artery Tibial'),('Brain_Basal_Ganglia','Brain Basal Ganglia'),('Brain_Cerebellum','Brain Cerebellum'),('Brain_Other','Brain Other'),('Breast','Breast'),('Colon_Sigmoid','Colon Sigmoid'),('Colon_Transverse','Colon Transverse'),('Esophagus_Mucosa','Esophagus Mucosa'),('Esophagus_Muscularis','Esophagus Muscularis'),('Fibroblast_Cell_Line','Fibroblast Cell Line'),('Gastroesophageal_Junction','Gastroesophageal Junction'),('Heart_Atrial_Appendage','Heart Atrial Appendage'),('Heart_Left_Ventricle','Heart Left Ventricle'),('Intestine_Terminal_Ileum','Intestine Terminal Ileum'),('Kidney_Cortex','Kidney Cortex'),('Lymphoblastoid_Cell_Line','Lymphoblastoid Cell Line'),('Minor_Salivary_Gland','Minor Salivary Gland'),('Liver','Liver'),('Lung','Lung'),('Ovary','Ovary'),('Pancreas','Pancreas'),('Pituitary','Pituitary'),('Prostate','Prostate'),('Skeletal_Muscle','Skeletal Muscle'),('Skin','Skin'),('Spleen','Spleen'),('Stomach','Stomach'),('Testis','Testis'),('Thyroid','Thyroid'),('Tibial_Nerve','Tibial Nerve'),('Uterus','Uterus'),('Vagina','Vagina'),('Whole_Blood','Whole Blood'),('ACC','Adrenocortical carcinoma - ACC'),('BLCA','Bladder Urothelial Carcinoma - BLCA'),('CHOL','Cholangiocarcinoma - CHOL'),('COAD','Colon adenocarcinoma - COAD'),('DLBC','Lymphoid Neoplasm Diffuse Large B-cell Lymphoma - DLBC'),('ESCA','Esophageal carcinoma - ESCA'),('GBM','	Glioblastoma multiforme - GBM'),('HNSC','Head and Neck squamous cell carcinoma - HNSC'),('KICH','Kidney Chromophobe - KICH'),('KIRC','Kidney renal clear cell carcinoma - KIRC'),('KIRP','Kidney renal papillary cell carcinoma - KIRP'),('LAML','Acute Myeloid Leukemia - LAML'),('LGG','Brain Lower Grade Glioma - LGG'),('LIHC','Liver hepatocellular carcinoma - LIHC'),('LUAD','Lung adenocarcinoma - LUAD'),('LUSC','	Lung squamous cell carcinoma - LUSC'),('MESO','Mesothelioma - MESO'),('PAAD','Pancreatic adenocarcinoma - PAAD'),('PCPG','Pheochromocytoma and Paraganglioma - PCPG'),('READ','Rectum adenocarcinoma - READ'),('SARC','Sarcoma - SARC'),('SKCM','Skin Cutaneous Melanoma - SKCM'),('STAD','Stomach adenocarcinoma - STAD'),('THCA','Thyroid carcinoma - THCA'),('THYM','Thymoma - THYM'),('UVM','Uveal Melanoma - UVM')]
    CHOICES5  = [('ACC','Adrenocortical carcinoma - ACC'),('BLCA','Bladder Urothelial Carcinoma - BLCA'),('CHOL','Cholangiocarcinoma - CHOL'),('COAD','Colon adenocarcinoma - COAD'),('DLBC','Lymphoid Neoplasm Diffuse Large B-cell Lymphoma - DLBC'),('ESCA','Esophageal carcinoma - ESCA'),('GBM','	Glioblastoma multiforme - GBM'),('HNSC','Head and Neck squamous cell carcinoma - HNSC'),('KICH','Kidney Chromophobe - KICH'),('KIRC','Kidney renal clear cell carcinoma - KIRC'),('KIRP','Kidney renal papillary cell carcinoma - KIRP'),('LAML','Acute Myeloid Leukemia - LAML'),('LGG','Brain Lower Grade Glioma - LGG'),('LIHC','Liver hepatocellular carcinoma - LIHC'),('LUAD','Lung adenocarcinoma - LUAD'),('LUSC','	Lung squamous cell carcinoma - LUSC'),('MESO','Mesothelioma - MESO'),('PAAD','Pancreatic adenocarcinoma - PAAD'),('PCPG','Pheochromocytoma and Paraganglioma - PCPG'),('READ','Rectum adenocarcinoma - READ'),('SARC','Sarcoma - SARC'),('SKCM','Skin Cutaneous Melanoma - SKCM'),('STAD','Stomach adenocarcinoma - STAD'),('THCA','Thyroid carcinoma - THCA'),('THYM','Thymoma - THYM'),('UVM','Uveal Melanoma - UVM'),('Adipose_Subcutaneous','Adipose Subcutaneous'),('Adipose_Visceral','Adipose Visceral'),('Adrenal_Gland','Adrenal Gland'),('Artery_Aorta','Artery Aorta'),('Artery_Coronary','Artery Coronary'),('Artery_Tibial','Artery Tibial'),('Brain_Basal_Ganglia','Brain Basal Ganglia'),('Brain_Cerebellum','Brain Cerebellum'),('Brain_Other','Brain Other'),('Breast','Breast'),('Colon_Sigmoid','Colon Sigmoid'),('Colon_Transverse','Colon Transverse'),('Esophagus_Mucosa','Esophagus Mucosa'),('Esophagus_Muscularis','Esophagus Muscularis'),('Fibroblast_Cell_Line','Fibroblast Cell Line'),('Gastroesophageal_Junction','Gastroesophageal Junction'),('Heart_Atrial_Appendage','Heart Atrial Appendage'),('Heart_Left_Ventricle','Heart Left Ventricle'),('Intestine_Terminal_Ileum','Intestine Terminal Ileum'),('Kidney_Cortex','Kidney Cortex'),('Lymphoblastoid_Cell_Line','Lymphoblastoid Cell Line'),('Minor_Salivary_Gland','Minor Salivary Gland'),('Liver','Liver'),('Lung','Lung'),('Ovary','Ovary'),('Pancreas','Pancreas'),('Pituitary','Pituitary'),('Prostate','Prostate'),('Skeletal_Muscle','Skeletal Muscle'),('Skin','Skin'),('Spleen','Spleen'),('Stomach','Stomach'),('Testis','Testis'),('Thyroid','Thyroid'),('Tibial_Nerve','Tibial Nerve'),('Uterus','Uterus'),('Vagina','Vagina'),('Whole_Blood','Whole Blood')]
    comp1     = forms.ChoiceField(choices=CHOICES4, widget=forms.Select)
    comp2     = forms.ChoiceField(choices=CHOICES5, widget=forms.Select)
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
        model = compmod
        fields = '__all__'

class DiffTarForm(forms.ModelForm):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES3  = [('nosel',''),('by gene',''),('by GO',''),('by GWAS','')]
    CHOICES4  = [('Adipose_Subcutaneous','Adipose Subcutaneous'),('Adipose_Visceral','Adipose Visceral'),('Adrenal_Gland','Adrenal Gland'),('Artery_Aorta','Artery Aorta'),('Artery_Coronary','Artery Coronary'),('Artery_Tibial','Artery Tibial'),('Brain_Basal_Ganglia','Brain Basal Ganglia'),('Brain_Cerebellum','Brain Cerebellum'),('Brain_Other','Brain Other'),('Breast','Breast'),('Colon_Sigmoid','Colon Sigmoid'),('Colon_Transverse','Colon Transverse'),('Esophagus_Mucosa','Esophagus Mucosa'),('Esophagus_Muscularis','Esophagus Muscularis'),('Fibroblast_Cell_Line','Fibroblast Cell Line'),('Gastroesophageal_Junction','Gastroesophageal Junction'),('Heart_Atrial_Appendage','Heart Atrial Appendage'),('Heart_Left_Ventricle','Heart Left Ventricle'),('Intestine_Terminal_Ileum','Intestine Terminal Ileum'),('Kidney_Cortex','Kidney Cortex'),('Lymphoblastoid_Cell_Line','Lymphoblastoid Cell Line'),('Minor_Salivary_Gland','Minor Salivary Gland'),('Liver','Liver'),('Lung','Lung'),('Ovary','Ovary'),('Pancreas','Pancreas'),('Pituitary','Pituitary'),('Prostate','Prostate'),('Skeletal_Muscle','Skeletal Muscle'),('Skin','Skin'),('Spleen','Spleen'),('Stomach','Stomach'),('Testis','Testis'),('Thyroid','Thyroid'),('Tibial_Nerve','Tibial Nerve'),('Uterus','Uterus'),('Vagina','Vagina'),('Whole_Blood','Whole Blood'),('ACC','Adrenocortical carcinoma - ACC'),('BLCA','Bladder Urothelial Carcinoma - BLCA'),('CHOL','Cholangiocarcinoma - CHOL'),('COAD','Colon adenocarcinoma - COAD'),('DLBC','Lymphoid Neoplasm Diffuse Large B-cell Lymphoma - DLBC'),('ESCA','Esophageal carcinoma - ESCA'),('GBM','	Glioblastoma multiforme - GBM'),('HNSC','Head and Neck squamous cell carcinoma - HNSC'),('KICH','Kidney Chromophobe - KICH'),('KIRC','Kidney renal clear cell carcinoma - KIRC'),('KIRP','Kidney renal papillary cell carcinoma - KIRP'),('LAML','Acute Myeloid Leukemia - LAML'),('LGG','Brain Lower Grade Glioma - LGG'),('LIHC','Liver hepatocellular carcinoma - LIHC'),('LUAD','Lung adenocarcinoma - LUAD'),('LUSC','	Lung squamous cell carcinoma - LUSC'),('MESO','Mesothelioma - MESO'),('PAAD','Pancreatic adenocarcinoma - PAAD'),('PCPG','Pheochromocytoma and Paraganglioma - PCPG'),('READ','Rectum adenocarcinoma - READ'),('SARC','Sarcoma - SARC'),('SKCM','Skin Cutaneous Melanoma - SKCM'),('STAD','Stomach adenocarcinoma - STAD'),('THCA','Thyroid carcinoma - THCA'),('THYM','Thymoma - THYM'),('UVM','Uveal Melanoma - UVM')]
    CHOICES5  = [('ACC','Adrenocortical carcinoma - ACC'),('BLCA','Bladder Urothelial Carcinoma - BLCA'),('CHOL','Cholangiocarcinoma - CHOL'),('COAD','Colon adenocarcinoma - COAD'),('DLBC','Lymphoid Neoplasm Diffuse Large B-cell Lymphoma - DLBC'),('ESCA','Esophageal carcinoma - ESCA'),('GBM','	Glioblastoma multiforme - GBM'),('HNSC','Head and Neck squamous cell carcinoma - HNSC'),('KICH','Kidney Chromophobe - KICH'),('KIRC','Kidney renal clear cell carcinoma - KIRC'),('KIRP','Kidney renal papillary cell carcinoma - KIRP'),('LAML','Acute Myeloid Leukemia - LAML'),('LGG','Brain Lower Grade Glioma - LGG'),('LIHC','Liver hepatocellular carcinoma - LIHC'),('LUAD','Lung adenocarcinoma - LUAD'),('LUSC','	Lung squamous cell carcinoma - LUSC'),('MESO','Mesothelioma - MESO'),('PAAD','Pancreatic adenocarcinoma - PAAD'),('PCPG','Pheochromocytoma and Paraganglioma - PCPG'),('READ','Rectum adenocarcinoma - READ'),('SARC','Sarcoma - SARC'),('SKCM','Skin Cutaneous Melanoma - SKCM'),('STAD','Stomach adenocarcinoma - STAD'),('THCA','Thyroid carcinoma - THCA'),('THYM','Thymoma - THYM'),('UVM','Uveal Melanoma - UVM'),('Adipose_Subcutaneous','Adipose Subcutaneous'),('Adipose_Visceral','Adipose Visceral'),('Adrenal_Gland','Adrenal Gland'),('Artery_Aorta','Artery Aorta'),('Artery_Coronary','Artery Coronary'),('Artery_Tibial','Artery Tibial'),('Brain_Basal_Ganglia','Brain Basal Ganglia'),('Brain_Cerebellum','Brain Cerebellum'),('Brain_Other','Brain Other'),('Breast','Breast'),('Colon_Sigmoid','Colon Sigmoid'),('Colon_Transverse','Colon Transverse'),('Esophagus_Mucosa','Esophagus Mucosa'),('Esophagus_Muscularis','Esophagus Muscularis'),('Fibroblast_Cell_Line','Fibroblast Cell Line'),('Gastroesophageal_Junction','Gastroesophageal Junction'),('Heart_Atrial_Appendage','Heart Atrial Appendage'),('Heart_Left_Ventricle','Heart Left Ventricle'),('Intestine_Terminal_Ileum','Intestine Terminal Ileum'),('Kidney_Cortex','Kidney Cortex'),('Lymphoblastoid_Cell_Line','Lymphoblastoid Cell Line'),('Minor_Salivary_Gland','Minor Salivary Gland'),('Liver','Liver'),('Lung','Lung'),('Ovary','Ovary'),('Pancreas','Pancreas'),('Pituitary','Pituitary'),('Prostate','Prostate'),('Skeletal_Muscle','Skeletal Muscle'),('Skin','Skin'),('Spleen','Spleen'),('Stomach','Stomach'),('Testis','Testis'),('Thyroid','Thyroid'),('Tibial_Nerve','Tibial Nerve'),('Uterus','Uterus'),('Vagina','Vagina'),('Whole_Blood','Whole Blood')]
    comp11     = forms.ChoiceField(choices=CHOICES4, widget=forms.Select)
    comp22     = forms.ChoiceField(choices=CHOICES5, widget=forms.Select)
    absvaltar    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    tfgeneseltar = forms.ChoiceField(choices=CHOICES3, widget=forms.RadioSelect)
    topbottomtar = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    nedgestar = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '250', 'value':'100','id':'myEdgeTar'}), required=False
    )
    absvaltartf    = forms.BooleanField(widget=forms.CheckboxInput, required = False )
    topbottomtartf = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    nedgestartf = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type':'range', 'step': '10', 'min': '50', 'max': '250', 'value':'100','id':'myEdgeTartf'}), required=False
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
        model = difftarmod
        fields = '__all__'