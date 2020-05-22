from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CellSerializer, TissuelandingSerializer, DruglandingSerializer, CancerlandingSerializer, GenelandingSerializer
from .models import DrugResultUp, DrugResultDown, Disease, Gwas, TissueTar, TissueEx, Cell, Druglanding, Tissuelanding, Cancerlanding
from .models import Genelanding
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_datatables.filters import DatatablesFilterBackend

class DruglandingList(ListAPIView):
        queryset         = Druglanding.objects.all()
        serializer_class = DruglandingSerializer
        #pagination_class = DrugResultPagination
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class CellList(ListAPIView):
        queryset         = Cell.objects.all()
        serializer_class = CellSerializer
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class TissuelandingList(ListAPIView):
        queryset         = Tissuelanding.objects.all()
        serializer_class = TissuelandingSerializer
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class CancerlandingList(ListAPIView):
        queryset         = Cancerlanding.objects.all()
        serializer_class = CancerlandingSerializer
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class GenelandingList(ListAPIView):
        queryset         = Genelanding.objects.all()
        serializer_class = GenelandingSerializer
