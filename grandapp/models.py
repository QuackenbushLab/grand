from django.db import models

class Cell(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    cellLine  = models.CharField(max_length=200)
    cellLink  = models.URLField(default='#')
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooLink= models.URLField(max_length=200)
    netzooRel = models.FloatField()
    network   = models.URLField()
    ppi       = models.URLField()
    ppiLink   = models.URLField()
    motif     = models.URLField()
    expression= models.URLField()
    expLink   = models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()
    #submitter = models.CharField(max_length=100)
    #species = models.CharField(max_length=30)
    #breed = models.CharField(max_length=30, blank=True)
    #description = models.TextField()
    #sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank=True)
    #submission_date = models.DateTimeField()
    #age = models.IntegerField(null=True)
    #vaccinations = models.ManyToManyField('Vaccine', blank=True)

class Drug(models.Model):
    number    = models.IntegerField(default='0')
    drug      = models.CharField(max_length=400)
    tool      = models.CharField(max_length=400)
    netzoo    = models.CharField(max_length=400)
    network   = models.CharField(max_length=400)
    ppi       = models.CharField(max_length=400)
    motif     = models.CharField(max_length=400)
    expression= models.CharField(max_length=400)
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()

class DrugResult(models.Model):
    id        = models.AutoField(primary_key=True)
    drug      = models.CharField(max_length=400)
    overlap   = models.FloatField()
    cosine    = models.FloatField()
    def __repr__(self):
        return '<DrugResult object ({}) "{}">'.format(self.id, self.drug)

class Tissue(models.Model):
    #SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    tissue    = models.CharField(max_length=200)
    tissueLink= models.URLField(default='#')
    tool      = models.CharField(max_length=200)
    netzoo    = models.CharField(max_length=200)
    netzooLink= models.URLField(max_length=200)
    netzooRel = models.FloatField()
    network   = models.URLField()
    ppi       = models.URLField()
    ppiLink   = models.URLField()
    motif     = models.URLField()
    expression= models.URLField()
    expLink   = models.URLField()
    tfs       = models.IntegerField()
    genes     = models.IntegerField()
    refs      = models.URLField()

    def __str__(self):
       return self.name

    def natural_key(self):
       return self.my_natural_key
