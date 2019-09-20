from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DrugSerializer, DrugResultSerializerUp, DrugResultSerializerDown, ParamsSerializer
from .models import Drug, DrugResultUp, DrugResultDown, Params
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

class DrugResultPagination(LimitOffsetPagination):
	default_limit = 100
	max_limit = 100

class DrugList(ListAPIView):
	queryset = Drug.objects.all()
	serializer_class = DrugSerializer
	#pagination_class = DrugResultPagination

class DrugResultListUp(ListAPIView):
	queryset = DrugResultUp.objects.all().order_by('overlap')
	serializer_class = DrugResultSerializerUp
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('id',)
	#pagination_class = DrugResultPagination

class DrugResultListDown(ListAPIView):
        queryset = DrugResultDown.objects.all().order_by('-overlap')
        serializer_class = DrugResultSerializerDown
        filter_backends = (DjangoFilterBackend,)
        filter_fields = ('id',)

class DrugRetrieveUpdateDestroyUp(RetrieveUpdateDestroyAPIView):
	queryset = DrugResultUp.objects.all()
	lookup_field = 'id'
	serializer_class = DrugResultSerializerUp

	def delete(self, request, *args, **kwargs):
		drugResult_id = request.data.get('id')
		response = super().delete(request, *args, **kwargs)
		if response.status_code == 204:
			from django.core.cache import cache
			cache.delete('drugResult_data_{}'.format(drugResult_id))
		return response

	def update(self, request, *args, **kwargs):
		response = super().update(request, *args, **kwargs)
		if response.status_code == 200:
			from django.core.cache import cache
			drugResult = response.data
			cache.set('drugResult_data_{}'.format(drugResult['id']), {
                                'drug': drugResult['drug'],
				'overlap': drugResult['overlap'],
				'cosine': drugResult['cosine'],
			})
		return response

class DrugRetrieveUpdateDestroyDown(RetrieveUpdateDestroyAPIView):
        queryset = DrugResultDown.objects.all()
        lookup_field = 'id'
        serializer_class = DrugResultSerializerDown

        def delete(self, request, *args, **kwargs):
                drugResult_id = request.data.get('id')
                response = super().delete(request, *args, **kwargs)
                if response.status_code == 204:
                        from django.core.cache import cache
                        cache.delete('drugResult_data_{}'.format(drugResult_id))
                return response

        def update(self, request, *args, **kwargs):
                response = super().update(request, *args, **kwargs)
                if response.status_code == 200:
                        from django.core.cache import cache
                        drugResult = response.data
                        cache.set('drugResult_data_{}'.format(drugResult['id']), {
                                'drug': drugResult['drug'],
                                'overlap': drugResult['overlap'],
                                'cosine': drugResult['cosine'],
                        })
                return response

class ParamRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
        queryset = Params.objects.all()
        lookup_field = 'id'
        serializer_class = ParamsSerializer

        def update(self, request, *args, **kwargs):
                response = super().update(request, *args, **kwargs)
                if response.status_code == 200:
                        from django.core.cache import cache
                        param = response.data
                        cache.set('param_data_{}'.format(param['id']), {
                                'genesupin': param['genesupin'],
                                'genesdownin': param['genesdownin'],
                                'genesup': param['genesup'],
                                'genesdown': param['genesdown'],
                        })
                return response
