from django.db import models

class Celllanding(models.Model):
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
    script    = models.CharField(max_length=200)
    dataset   = models.CharField(max_length=200)
    cancerref = models.CharField(max_length=200)
    reg = models.CharField(max_length=200)

class Cell(models.Model):
    disease    = models.CharField(max_length=400)
    ncells     = models.IntegerField()

class Cellpage(models.Model):
    tissue   = models.CharField(max_length=400)
    method   = models.CharField(max_length=400)
    data     = models.CharField(max_length=400)
    typenet  = models.CharField(max_length=400)
    condition=  models.CharField(max_length=400)
    methodrefs   = models.CharField(max_length=400)
    datarefs     = models.CharField(max_length=400)
    urllinks     = models.CharField(max_length=400)
    reg       = models.CharField(max_length=400)
    reg2      = models.CharField(max_length=400)
    method2   = models.CharField(max_length=400)
    methodrefs2  = models.CharField(max_length=400)

class Cellsample(models.Model):
    depmap        = models.CharField(max_length=400)
    stripcellname = models.CharField(max_length=400)
    cclename      = models.CharField(max_length=400)
    cosmicid      = models.CharField(max_length=400)
    sex           = models.CharField(max_length=400)
    source        = models.CharField(max_length=400)
    culture       = models.CharField(max_length=400)
    cas9act       = models.CharField(max_length=400)
    collsite      = models.CharField(max_length=400)
    prim          = models.CharField(max_length=400)
    disease       = models.CharField(max_length=400)
    subtype       = models.CharField(max_length=400)
    age           = models.CharField(max_length=400)
    mutrate       = models.CharField(max_length=400)
    doublt        = models.CharField(max_length=400)
    tcga          = models.CharField(max_length=400)
    link          = models.CharField(max_length=400)
    race          = models.CharField(max_length=400)
    size          = models.CharField(max_length=400)

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
    altid           = models.CharField(max_length=400)
    inchi_key_prefix= models.CharField(max_length=400)
    inchi_key       = models.CharField(max_length=400)
    canonical_smiles= models.CharField(max_length=400)
    pubchem_cid     = models.CharField(max_length=400)
    orig      = models.CharField(max_length=400)
    pval = models.FloatField(default=0.1)
    qval = models.FloatField(default=0.1)
    tval = models.FloatField(default=0.1)

class DrugResultDown(models.Model):
    idd       = models.IntegerField(default=0)
    drug      = models.CharField(max_length=400)
    overlap   = models.FloatField()
    cosine    = models.FloatField()
    druglink  = models.URLField()
    query     = models.IntegerField(default=0)
    nuser     = models.IntegerField(default=0)
    altid           = models.CharField(max_length=400)
    inchi_key_prefix= models.CharField(max_length=400)
    inchi_key       = models.CharField(max_length=400)
    canonical_smiles= models.CharField(max_length=400)
    pubchem_cid     = models.CharField(max_length=400)
    orig      = models.CharField(max_length=400)
    pval = models.FloatField(default=0.1)
    qval = models.FloatField(default=0.1)
    tval = models.FloatField(default=0.1)

class Drugcombsup(models.Model):
    drug1      = models.CharField(max_length=400)
    drug2      = models.CharField(max_length=400)
    cosine     = models.FloatField(default=0.1)
    abscosine     = models.FloatField(default=0.1)
    nuser      = models.IntegerField(default=0)
    idd        = models.IntegerField(default=0)
    query      = models.IntegerField(default=0)

class Drugcombsdown(models.Model):
    drug1      = models.CharField(max_length=400)
    drug2      = models.CharField(max_length=400)
    cosine     = models.FloatField(default=0.1)
    abscosine     = models.FloatField(default=0.1)
    nuser      = models.IntegerField(default=0)
    idd        = models.IntegerField(default=0)
    query      = models.IntegerField(default=0)

class Params(models.Model):
    id         = models.AutoField(primary_key=True)
    genesupin  = models.IntegerField(default=0)
    genesdownin= models.IntegerField(default=0)
    genesup    = models.IntegerField(default=0)
    genesdown  = models.IntegerField(default=0)
    query      = models.IntegerField(default=0)
    combin     = models.CharField(max_length=400)

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
    logpval      = models.FloatField()

class Gwas(models.Model):
    idd          = models.IntegerField(default=0)
    disease      = models.CharField(max_length=600)
    count        = models.IntegerField()
    intersect    = models.IntegerField()
    pval         = models.FloatField()
    qval         = models.FloatField()
    query        = models.IntegerField(default=0)
    nuser        = models.IntegerField(default=0)
    logpval      = models.FloatField()

class Tissue(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    tissue    = models.CharField(max_length=200)
    nnets     = models.IntegerField(default=0)

class Cancer(models.Model):
    tissue    = models.CharField(max_length=200)
    cancerref = models.CharField(max_length=200)
    nnets     = models.CharField(max_length=200)
    nnets2    = models.CharField(max_length=200)
    nnetsref  = models.CharField(max_length=200)
    nnets2ref = models.CharField(max_length=200)
    datasets  = models.CharField(max_length=200)
    datasets2  = models.CharField(max_length=200)
    datasetsref  = models.CharField(max_length=200)
    datasets2ref  = models.CharField(max_length=200)
    types     = models.CharField(max_length=200)
    subtype   = models.CharField(max_length=200)

class Tissuelanding(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    tissue    = models.CharField(max_length=200)
    tissueLink= models.URLField(default='#')
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooLink= models.URLField(max_length=200)
    netzooRel = models.CharField(max_length=200)
    reg       = models.CharField(max_length=200)
    network   = models.URLField()
    ppi       = models.URLField()
    ppiLink   = models.URLField()
    motif     = models.URLField()
    motifDesc = models.CharField(max_length=200)
    expression= models.URLField()
    expLink   = models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()
    refs2     = models.URLField(default='#')
    refs3     = models.URLField(default='#')
    samples   = models.IntegerField(default=0)
    script    = models.CharField(max_length=200)

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
    logpval      = models.FloatField()

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
    smtstptref  = models.CharField(max_length=600)

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

class Breastsample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    sample     = models.CharField(max_length=200)
    gender     = models.CharField(max_length=200)
    race       = models.CharField(max_length=200)
    ethnicity  = models.CharField(max_length=200)
    weight_kg_at_diagnosis  = models.CharField(max_length=200)
    height_cm_at_diagnosis  = models.CharField(max_length=200)
    age_at_initial_pathologic_diagnosis  = models.CharField(max_length=200)
    primary_site        = models.CharField(max_length=200)
    primary_diagnosis        = models.CharField(max_length=200)
    uicc_stage   = models.CharField(max_length=200)
    time_to_event= models.CharField(max_length=200)
    vital_status = models.CharField(max_length=200)

class Cervixsample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    sample     = models.CharField(max_length=200)
    gender     = models.CharField(max_length=200)
    race       = models.CharField(max_length=200)
    ethnicity  = models.CharField(max_length=200)
    weight_kg_at_diagnosis  = models.CharField(max_length=200)
    height_cm_at_diagnosis  = models.CharField(max_length=200)
    age_at_initial_pathologic_diagnosis  = models.CharField(max_length=200)
    primary_site        = models.CharField(max_length=200)
    primary_diagnosis        = models.CharField(max_length=200)
    uicc_stage   = models.CharField(max_length=200)
    time_to_event= models.CharField(max_length=200)
    vital_status = models.CharField(max_length=200)

class Liversample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    sample     = models.CharField(max_length=200)
    gender     = models.CharField(max_length=200)
    race       = models.CharField(max_length=200)
    ethnicity  = models.CharField(max_length=200)
    weight_kg_at_diagnosis  = models.CharField(max_length=200)
    height_cm_at_diagnosis  = models.CharField(max_length=200)
    age_at_initial_pathologic_diagnosis  = models.CharField(max_length=200)
    primary_site        = models.CharField(max_length=200)
    primary_diagnosis        = models.CharField(max_length=200)
    uicc_stage   = models.CharField(max_length=200)
    time_to_event= models.CharField(max_length=200)
    vital_status = models.CharField(max_length=200)

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

class Ggnsample(models.Model):
    sample     = models.CharField(max_length=200)
    survival = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

class Cancerlanding(models.Model):
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
    script    = models.CharField(max_length=200)
    dataset   = models.CharField(max_length=200)

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
    infl            = models.CharField(max_length=200) 
    links           = models.CharField(max_length=200)
    linksTF         = models.CharField(max_length=200)

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
    logpval      = models.FloatField()

class Ggbmd1sample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    submitter_id        = models.CharField(max_length=200)
    yearstobirth        = models.CharField(max_length=200)
    vitalstatus         = models.CharField(max_length=200)
    daystodeath         = models.CharField(max_length=200)
    daystolastfollowup  = models.CharField(max_length=200)
    gender              = models.CharField(max_length=200)
    dateofinitialpathologicdiagnosis  = models.CharField(max_length=200)
    radiationtherapy    = models.CharField(max_length=200)
    karnofskyperformancescore        = models.CharField(max_length=200)
    histologicaltype    = models.CharField(max_length=200)
    radiationsradiationregimenindication= models.CharField(max_length=200)
    race                = models.CharField(max_length=200)
    ethnicity           = models.CharField(max_length=200)
    neoadjuvanttherapy  = models.CharField(max_length=200)
    size                = models.CharField(max_length=200)
    link                = models.CharField(max_length=200)
    platform            = models.CharField(max_length=200)

class Ggbmd2sample(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    submitter_id        = models.CharField(max_length=200)
    yearstobirth        = models.CharField(max_length=200)
    vitalstatus         = models.CharField(max_length=200)
    daystodeath         = models.CharField(max_length=200)
    daystolastfollowup  = models.CharField(max_length=200)
    gender              = models.CharField(max_length=200)
    dateofinitialpathologicdiagnosis  = models.CharField(max_length=200)
    radiationtherapy    = models.CharField(max_length=200)
    karnofskyperformancescore        = models.CharField(max_length=200)
    histologicaltype    = models.CharField(max_length=200)
    radiationsradiationregimenindication= models.CharField(max_length=200)
    race                = models.CharField(max_length=200)
    ethnicity           = models.CharField(max_length=200)
    neoadjuvanttherapy  = models.CharField(max_length=200)
    size                = models.CharField(max_length=200)
    link                = models.CharField(max_length=200)
    platform            = models.CharField(max_length=200)

class Pancreassample(models.Model):
    sample     = models.CharField(max_length=200)
    race       = models.CharField(max_length=200)
    gender     = models.CharField(max_length=200)
    primary_site       = models.CharField(max_length=200)
    ethnicity          = models.CharField(max_length=200)
    primary_diagnosis  = models.CharField(max_length=200)
    age_at_initial_pathologic_diagnosis	         = models.CharField(max_length=200)
    uicc_stage	 = models.CharField(max_length=200)
    time_to_event= models.CharField(max_length=200)
    vital_status = models.CharField(max_length=200)
    size         = models.CharField(max_length=200)
    link         = models.CharField(max_length=200)
    subtype      = models.CharField(max_length=200)

class Otterac(models.Model):
    aurocbr      = models.FloatField()
    auroccer     = models.FloatField()
    aurocliv     = models.FloatField()
    auprbr       = models.FloatField()
    auprcer      = models.FloatField()
    auprliv      = models.FloatField()
    method       = models.CharField(max_length=200)

class Pandaac(models.Model):
    ko     = models.FloatField()
    cc     = models.FloatField()
    sr     = models.FloatField()
    method       = models.CharField(max_length=200)

class Dragonac(models.Model):
    ko     = models.FloatField()
    cc     = models.FloatField()
    method       = models.CharField(max_length=200)

class Gobp(models.Model):
    term      = models.CharField(max_length=400)
    goid      = models.CharField(max_length=400)
    genelist  = models.CharField(max_length=3000)
    idd       = models.IntegerField()

class Gwascata(models.Model):
    term      = models.CharField(max_length=400)
    genelist  = models.CharField(max_length=3000)
    idd       = models.IntegerField()

class Sendto(models.Model):
    preload       = models.IntegerField(default=0)
    idd           = models.IntegerField(default=0)
    genelistup    = models.CharField(max_length=10000)
    genelistdown  = models.CharField(max_length=10000)

class Gobpbygene(models.Model):
    gene      = models.CharField(max_length=400)
    termlist  = models.CharField(max_length=3000)

class Gwascatabygene(models.Model):
    gene      = models.CharField(max_length=400)
    termlist  = models.CharField(max_length=3000)

class Lala(models.Model):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES2  = [('Histone','Histone'),('CNV','CNV'),('Methylation','Methylation'),('miRNA','miRNA'),('mRNA','mRNA'),
    ('Protein','Protein'),('Metabolism','Metabolism'),('Drugs','Drugs'),('Dependency','Dependency')]
    topbottom = models.CharField(choices=CHOICES, max_length=200)
    connex    = models.CharField(choices=CHOICES2, max_length=200)
    methyl    = models.BooleanField()
    mir       = models.BooleanField()
    hm        = models.BooleanField()
    dep       = models.BooleanField()
    exp       = models.BooleanField()
    prot      = models.BooleanField()
    met       = models.BooleanField()
    cnv       = models.BooleanField()
    agg       = models.BooleanField()
    absval    = models.BooleanField()
    nedges    = models.IntegerField()
    gp        = models.BooleanField()
    allay     = models.BooleanField()

    def __str__(self):
       return self.name

    def natural_key(self):
       return self.my_natural_key


class netmod(models.Model):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES2  = [('no',''),('dtt',''),('dee',''),('bc','')]
    CHOICES3  = [('nosel','nosel'),('by gene','by gene'),('by tf','by tf'),('by GO','by GO'),('by GWAS','by GWAS')]
    dt        = models.CharField(choices=CHOICES2, max_length=200)
    topbottom = models.CharField(choices=CHOICES, max_length=200)
    brd       = models.BooleanField()
    nedges    = models.IntegerField()
    absval    = models.BooleanField()
    tfgenesel = models.CharField(choices=CHOICES3, max_length=200)
    geneform  = models.CharField(max_length=200)
    tfform    = models.CharField(max_length=200)
    goform    = models.CharField(max_length=200)
    gwasform    = models.CharField(max_length=200)

    def __str__(self):
       return self.name

    def natural_key(self):
       return self.my_natural_key

class tarmod(models.Model):
    CHOICES   = [('Largest','Largest'),('Smallest','Smallest')]
    CHOICES3  = [('nosel','nosel'),('by gene','by gene'),('by GO','by GO'),('by GWAS','by GWAS')]
    tfgeneseltar = models.CharField(choices=CHOICES3, max_length=200)
    topbottomtar = models.CharField(choices=CHOICES, max_length=200)
    nedgestar    = models.IntegerField()
    absvaltar    = models.BooleanField()
    topbottomtartf= models.CharField(choices=CHOICES, max_length=200)
    nedgestartf   = models.IntegerField()
    absvaltartf   = models.BooleanField()
    geneformtar   = models.CharField(max_length=200)
    goformtar     = models.CharField(max_length=200)
    gwasformtar   = models.CharField(max_length=200)

    def __str__(self):
       return self.name

    def natural_key(self):
       return self.my_natural_key


