from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DrugSerializer, DrugResultSerializerUp, DrugResultSerializerDown, ParamsSerializer, DiseaseSerializer, GwasSerializer
from .models import Drug, DrugResultUp, DrugResultDown, Params, Disease, Gwas
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework_datatables.filters import DatatablesFilterBackend

class DrugResultPagination(LimitOffsetPagination):
	default_limit = 100
	max_limit = 100

class DrugList(ListAPIView):
	queryset = Drug.objects.all()
	serializer_class = DrugSerializer
	#pagination_class = DrugResultPagination

class DrugResultListUp(ListAPIView):
	queryset = DrugResultUp.objects.all()
	serializer_class = DrugResultSerializerUp
	filter_backends = (DatatablesFilterBackend,DjangoFilterBackend,)
	filter_fields = ('query',)
	#search_fields = ('drug',)
	#pagination_class = DrugResultPagination

class DrugResultListDown(ListAPIView):
        queryset = DrugResultDown.objects.all()
        serializer_class = DrugResultSerializerDown
        filter_backends = (DatatablesFilterBackend,DjangoFilterBackend,)
        filter_fields = ('query',)

class DiseaseList(ListAPIView):
        queryset = Disease.objects.all()
        serializer_class = DiseaseSerializer
        filter_backends = (DjangoFilterBackend,DatatablesFilterBackend,)
        filter_fields = ('query',)

class GwasList(ListAPIView):
        queryset = Gwas.objects.all()
        serializer_class = GwasSerializer
        filter_backends = (DjangoFilterBackend,DatatablesFilterBackend,)
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
