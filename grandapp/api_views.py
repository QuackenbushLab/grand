from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from .serializers import DrugSerializer, DrugResultSerializer
from .models import Drug, DrugResult
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

class DrugResultPagination(LimitOffsetPagination):
	default_limit = 10
	max_limit = 100

class DrugList(ListAPIView):
	queryset = Drug.objects.all()
	serializer_class = DrugSerializer
	pagination_class = DrugResultPagination

class DrugResultList(ListAPIView):
	queryset = DrugResult.objects.all()
	serializer_class = DrugResultSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('id',)
	pagination_class = DrugResultPagination

class DrugRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
	queryset = DrugResult.objects.all()
	lookup_field = 'id'
	serializer_class = DrugResultSerializer

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
