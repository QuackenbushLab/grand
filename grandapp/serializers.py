from rest_framework import serializers

from .models import Drug

class DrugSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Drug
		fields = ('number','drug','tool','netzoo','network','ppi','motif','expression','tfs','genes','refs')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		#data['is_on_sale'] = instance.is_on_sale()
		#data['current_price'] = instance.current_price()
		return data