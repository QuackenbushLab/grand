from rest_framework import serializers

from .models import Drug, Disease, Cell, Tissue, Tissuelanding, Druglanding

class DrugSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Drug
		fields = ('number','drug','nnets')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		#data['is_on_sale'] = instance.is_on_sale()
		#data['current_price'] = instance.current_price()
		return data

class TissuelandingSerializer(serializers.ModelSerializer):
        class Meta:
                model = Tissuelanding
                fields = ('tissue','tissueLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression','expLink','tfs','genes','refs','refs2','samples')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class CellSerializer(serializers.ModelSerializer):
        class Meta:
                model = Cell
                fields = ('cellLine','cellLink','tool','netzoo','netzooLink','network','ppi','ppiLink','motif','expression','expLink','tfs','genes','refs')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class DruglandingSerializer(serializers.ModelSerializer):
        class Meta:
                model  = Druglanding
                fields = ('number','drug','tool','netzoo','netzooRel','network','ppi','motif','expression','tfs','genes','ppiLink','refs','samples','expLink')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                #data['is_on_sale'] = instance.is_on_sale()
                #data['current_price'] = instance.current_price()
                return data
