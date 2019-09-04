from rest_framework.generics import ListAPIView
from  .serializers import DrugSerializer 
from .models import Drug

class DrugList(ListAPIView):
	queryset = Drug.objects.all()
	serializer_class = DrugSerializer

