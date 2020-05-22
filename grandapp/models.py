from django.db import models

class Cell(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    cellLine  = models.CharField(max_length=200)
    cellLink  = models.URLField(default='#')
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooLink= models.URLField(max_length=200)
    netzooRel = models.CharField(max_length=200)
    network   = models.URLField()
    ppi       = models.URLField()
    ppiLink   = models.URLField()
    motif     = models.URLField()
    expression= models.URLField()
    expLink   = models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()
    samples   = models.IntegerField(default=0)
    #submitter = models.CharField(max_length=100)
    #species = models.CharField(max_length=30)
    #breed = models.CharField(max_length=30, blank=True)
    #description = models.TextField()
    #sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank=True)
    #submission_date = models.DateTimeField()
    #age = models.IntegerField(null=True)
    #vaccinations = models.ManyToManyField('Vaccine', blank=True)

class Druglanding(models.Model):
    number    = models.IntegerField(default=0)
    drug      = models.CharField(max_length=200)
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooRel = models.CharField(max_length=200)
    network   = models.URLField()
    ppi       = models.URLField()
    motif     = models.URLField()
    expression= models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    ppiLink   = models.CharField(max_length=200)
    refs      = models.URLField()
    samples   = models.IntegerField(default=0)
    expLink   = models.URLField()
    nnets     = models.IntegerField(default=0)
    druglink  = models.CharField(max_length=200)

class DrugResultUp(models.Model):
    idd       = models.IntegerField(default=0)
    drug      = models.CharField(max_length=400)
    overlap   = models.FloatField()
    cosine    = models.FloatField()
    druglink  = models.URLField()
    query     = models.IntegerField(default=0)
    nuser     = models.IntegerField(default=0)

class DrugResultDown(models.Model):
    idd       = models.IntegerField(default=0)
    drug      = models.CharField(max_length=400)
    overlap   = models.FloatField()
    cosine    = models.FloatField()
    druglink  = models.URLField()
    query     = models.IntegerField(default=0)
    nuser     = models.IntegerField(default=0)

class Params(models.Model):
    id         = models.AutoField(primary_key=True)
    genesupin  = models.IntegerField(default=0)
    genesdownin= models.IntegerField(default=0)
    genesup    = models.IntegerField(default=0)
    genesdown  = models.IntegerField(default=0)
    query      = models.IntegerField(default=0)

class Disease(models.Model):
    idd          = models.IntegerField(default=0)
    disease      = models.CharField(max_length=600)
    count        = models.IntegerField()
    intersect    = models.IntegerField()
    pval         = models.FloatField()
    qval         = models.FloatField()
    hpoId        = models.CharField(max_length=200)
    query        = models.IntegerField(default=0)
    nuser        = models.IntegerField(default=0)

class Gwas(models.Model):
    idd          = models.IntegerField(default=0)
    disease      = models.CharField(max_length=600)
    count        = models.IntegerField()
    intersect    = models.IntegerField()
    pval         = models.FloatField()
    qval         = models.FloatField()
    query        = models.IntegerField(default=0)
    nuser        = models.IntegerField(default=0)

class Tissue(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    tissue    = models.CharField(max_length=200)
    nnets     = models.IntegerField(default=0)

class Tissuelanding(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    tissue    = models.CharField(max_length=200)
    tissueLink= models.URLField(default='#')
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooLink= models.URLField(max_length=200)
    netzooRel = models.CharField(max_length=200)
    network   = models.URLField()
    ppi       = models.URLField()
    ppiLink   = models.URLField()
    motif     = models.URLField()
    expression= models.URLField()
    expLink   = models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()
    refs2     = models.URLField(default='#')
    samples   = models.IntegerField(default=0)

class TissueTar(models.Model):
    idd          = models.IntegerField(default=0)
    tissue       = models.CharField(max_length=600)
    count        = models.IntegerField()
    intersect    = models.IntegerField()
    pval         = models.FloatField()
    qval         = models.FloatField()
    tissueLink   = models.URLField('#')
    query        = models.IntegerField(default=0)
    nuser        = models.IntegerField(default=0)

class Tissuesample(models.Model):
    sampleid    = models.CharField(max_length=600)
    subjectid   = models.CharField(max_length=600)
    tissueid    = models.CharField(max_length=600)
    gender      = models.CharField(max_length=600)
    age         = models.CharField(max_length=600)
    dthhrdy     = models.CharField(max_length=600)
    smatsscr    = models.CharField(max_length=600)
    smrin       = models.CharField(max_length=600)
    smts        = models.CharField(max_length=600)
    smtsd       = models.CharField(max_length=600)
    smubrid     = models.CharField(max_length=600)
    smtsisch    = models.CharField(max_length=600)
    grdid       = models.CharField(max_length=600)
    size        = models.CharField(max_length=600)
    link        = models.CharField(max_length=600)

class Tcgasample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    sample     = models.CharField(max_length=200)
    platform   = models.CharField(max_length=200)
    gender     = models.CharField(max_length=200)
    race       = models.CharField(max_length=200)
    weight_kg_at_diagnosis  = models.CharField(max_length=200)
    height_cm_at_diagnosis  = models.CharField(max_length=200)
    age_at_initial_pathologic_diagnosis	 = models.CharField(max_length=200)
    anatomic_neoplasm_subdivision	 = models.CharField(max_length=200)
    uicc_stage	 = models.CharField(max_length=200)
    time_to_event= models.CharField(max_length=200)
    vital_status = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

class Geosample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    sample     = models.CharField(max_length=200)
    gender     = models.CharField(max_length=200)
    race       = models.CharField(max_length=200)
    geoid      = models.CharField(max_length=200)
    age_at_initial_pathologic_diagnosis  = models.CharField(max_length=200)
    tumor_location = models.CharField(max_length=200)
    uicc_stage   = models.CharField(max_length=200)
    time_to_event= models.CharField(max_length=200)
    vital_status = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

class Cancerlanding(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    cancer    = models.CharField(max_length=200)
    cancerLink= models.URLField(default='#')
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooLink= models.URLField(max_length=200)
    netzooRel = models.CharField(max_length=200)
    network   = models.URLField()
    ppi       = models.URLField()
    ppiLink   = models.URLField()
    motif     = models.URLField()
    expression= models.URLField()
    expLink   = models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()
    refs2     = models.URLField(default='#')
    samples   = models.IntegerField(default=0)
    cardref   = models.CharField(max_length=200)

class Genelanding(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    pr_gene_id    = models.CharField(max_length=200)
    pr_gene_symbol= models.CharField(max_length=200)
    pr_gene_title = models.CharField(max_length=200)
    pr_is_lm      = models.CharField(max_length=200)
    pr_is_bing    = models.CharField(max_length=200)

class Drugsample(models.Model):
    sig_id      = models.CharField(max_length=200)
    pert_iname  = models.CharField(max_length=200)
    cell_id     = models.CharField(max_length=200)
    pert_idose  = models.CharField(max_length=200)
    pert_itime  = models.CharField(max_length=200)
    distil_nsample  = models.CharField(max_length=200)
    cell_type       = models.CharField(max_length=200)
    modification    = models.CharField(max_length=200)
    sample_type     = models.CharField(max_length=200)
    primary_site    = models.CharField(max_length=200)
    subtype         = models.CharField(max_length=200)
    original_growth_pattern     = models.CharField(max_length=200)
    donor_age       = models.CharField(max_length=200)
    donor_sex       = models.CharField(max_length=200)
    donor_ethnicity = models.CharField(max_length=200)
    network         = models.CharField(max_length=200)
    size            = models.CharField(max_length=200)

class Drugdesc(models.Model):
    expected_mass  = models.CharField(max_length=200)
    smiles         = models.CharField(max_length=200)
    InChIKey       = models.CharField(max_length=200)
    pubchem_cid    = models.CharField(max_length=200)
    pert_iname     = models.CharField(max_length=200)
    clinical_phase = models.CharField(max_length=200)
    moa            = models.CharField(max_length=200)
    target         = models.CharField(max_length=200)
    disease_area   = models.CharField(max_length=200)
    indication     = models.CharField(max_length=200)
    broad_id       = models.CharField(max_length=200)
 
class TissueEx(models.Model):
    idd          = models.IntegerField(default=0)
    tissue       = models.CharField(max_length=600)
    count        = models.IntegerField()
    intersect    = models.IntegerField()
    pval         = models.FloatField()
    qval         = models.FloatField()
    tissueLink   = models.URLField('#')
    query        = models.IntegerField(default=0)
    nuser        = models.IntegerField(default=0)

    def __str__(self):
       return self.name

    def natural_key(self):
       return self.my_natural_key

