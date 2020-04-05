from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DrugSerializer
from .serializers import CellSerializer, TissuelandingSerializer, DruglandingSerializer
from .models import Drug, DrugResultUp, DrugResultDown, Disease, Gwas, TissueTar, TissueEx, Cell, Druglanding, Tissuelanding
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_datatables.filters import DatatablesFilterBackend

class DrugResultPagination(LimitOffsetPagination):
	default_limit = 20000
	max_limit = 20000

class DrugList(ListAPIView):
	queryset = Drug.objects.all()
	serializer_class = DrugSerializer
	#pagination_class = DrugResultPagination

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
