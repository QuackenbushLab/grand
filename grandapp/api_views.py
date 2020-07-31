from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CellSerializer, TissuelandingSerializer, DruglandingSerializer, CancerlandingSerializer, GenelandingSerializer
from .models import DrugResultUp, DrugResultDown, Disease, Gwas, TissueTar, TissueEx, Cell, Druglanding, Tissuelanding, Cancerlanding
from .models import Genelanding
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from django_filters.rest_framework import DjangoFilterBackend

class DruglandingList(ListAPIView):
        queryset         = Druglanding.objects.all()
        serializer_class = DruglandingSerializer
        #pagination_class = DrugResultPagination
        filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        filter_fields    = ('number','drug','tool','netzoo','netzooRel','tfs','genes','samples','nnets')

class CellList(ListAPIView):
        queryset         = Cell.objects.all()
        serializer_class = CellSerializer
        filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        filter_fields    = ('cellLine','tool','netzoo','tfs','genes')

class TissuelandingList(ListAPIView):
        queryset         = Tissuelanding.objects.all()
        serializer_class = TissuelandingSerializer
        filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        filter_fields    = ('tissue','tool','netzoo','netzooRel','tfs','genes','samples')

class CancerlandingList(ListAPIView):
        queryset         = Cancerlanding.objects.all()
        serializer_class = CancerlandingSerializer
        filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        filter_fields    = ('cancer','tool','netzoo','netzooRel','tfs','genes','samples')

class GenelandingList(ListAPIView):
        queryset         = Genelanding.objects.all()
        serializer_class = GenelandingSerializer
        filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        filter_fields    = ('pr_gene_id','pr_gene_symbol','pr_gene_title','pr_is_lm','pr_is_bing')
