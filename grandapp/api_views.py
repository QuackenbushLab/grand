from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DrugSerializer, DrugResultSerializerUp, DrugResultSerializerDown, ParamsSerializer, DiseaseSerializer, GwasSerializer, TissueTarSerializer, TissueExSerializer
from .serializers import CellSerializer, TissueSerializer, DrugApiSerializer
from .models import Drug, DrugResultUp, DrugResultDown, Params, Disease, Gwas, TissueTar, TissueEx, Tissue, Cell, DrugApi
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_datatables.filters import DatatablesFilterBackend

class DrugResultPagination(LimitOffsetPagination):
	default_limit = 20000
	max_limit = 20000

class DrugList(ListAPIView):
	queryset = Drug.objects.all()
	serializer_class = DrugSerializer
	#pagination_class = DrugResultPagination

class DrugApiList(ListAPIView):
        queryset         = DrugApi.objects.all()
        serializer_class = DrugApiSerializer
        #pagination_class = DrugResultPagination
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class CellList(ListAPIView):
        queryset         = Cell.objects.all()
        serializer_class = CellSerializer
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class TissueList(ListAPIView):
        queryset         = Tissue.objects.all()
        serializer_class = TissueSerializer
        #filter_backends  = (DatatablesFilterBackend,DjangoFilterBackend,)
        #filter_fields    = ('query',)

class DrugResultListUp(ListAPIView):
	queryset = DrugResultUp.objects.all()
	serializer_class = DrugResultSerializerUp
	filter_backends = (DatatablesFilterBackend,)
	filter_fields = ('query',)
	#search_fields = ('drug',)
	#pagination_class = DrugResultPagination

class DrugResultListDown(ListAPIView):
        queryset = DrugResultDown.objects.all()
        serializer_class = DrugResultSerializerDown
        filter_backends = (DatatablesFilterBackend,)
        filter_fields = ('query',)

class DiseaseList(ListAPIView):
        queryset = Disease.objects.all()
        serializer_class = DiseaseSerializer
        filter_backends = (DatatablesFilterBackend,)
        filter_fields = ('query',)

class GwasList(ListAPIView):
        queryset = Gwas.objects.all()
        serializer_class = GwasSerializer
        filter_backends = (DatatablesFilterBackend,)
        filter_fields = ('query',)

class TissueTarList(ListAPIView):
        queryset = TissueTar.objects.all()
        serializer_class = TissueTarSerializer
        filter_backends = (DatatablesFilterBackend,)
        filter_fields = ('query',)

class TissueExList(ListAPIView):
        queryset = TissueEx.objects.all()
        serializer_class = TissueExSerializer
        filter_backends = (DatatablesFilterBackend,)
        filter_fields = ('query',)

class DrugRetrieveUpdateDestroyUp(RetrieveUpdateDestroyAPIView):
	queryset = DrugResultUp.objects.all()
	lookup_field = 'id'
	serializer_class = DrugResultSerializerUp

class DrugRetrieveUpdateDestroyDown(RetrieveUpdateDestroyAPIView):
        queryset = DrugResultDown.objects.all()
        lookup_field = 'id'
        serializer_class = DrugResultSerializerDown

class ParamRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Params.objects.all()
        lookup_field = 'id'
        serializer_class = ParamsSerializer

class DiseaseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Disease.objects.all()
        lookup_field = 'id'
        serializer_class = DiseaseSerializer

class GwasRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Gwas.objects.all()
        lookup_field = 'id'
        serializer_class = GwasSerializer
