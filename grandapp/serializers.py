from rest_framework import serializers

from .models import Drug, DrugResultUp, DrugResultDown, Params, Disease, Gwas

class DrugSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Drug
		fields = ('number','drug','tool','netzoo','network','ppi','motif','expression','tfs','genes','refs')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		#data['is_on_sale'] = instance.is_on_sale()
		#data['current_price'] = instance.current_price()
		return data

class DrugResultSerializerUp(serializers.ModelSerializer):
	class Meta:
		model = DrugResultUp
		fields = ('id','drug','overlap','cosine')
	
	def to_representation(self, instance):
		data = super().to_representation(instance)
		return data

class DrugResultSerializerDown(serializers.ModelSerializer):
        class Meta:
                model = DrugResultDown
                fields = ('id','drug','overlap','cosine')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class ParamsSerializer(serializers.ModelSerializer):
        class Meta:
                model = Params
                fields = ('id','genesupin','genesdownin','genesup','genesdown')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class DiseaseSerializer(serializers.ModelSerializer):
        class Meta:
                model = Disease
                fields = ('id','disease','count','intersect','pval','qval')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class GwasSerializer(serializers.ModelSerializer):
        class Meta:
                model = Gwas
                fields = ('id','disease','count','intersect','pval','qval')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data
