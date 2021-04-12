from rest_framework import serializers

from .models import Disease, Cell, Tissue, Tissuelanding, Druglanding, Cancerlanding, Genelanding, Gobp

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

class GenelandingSerializer(serializers.ModelSerializer):
        class Meta:
                model = Genelanding
                fields = ('pr_gene_id','pr_gene_symbol','pr_gene_title','pr_is_lm','pr_is_bing')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class GobplandingSerializer(serializers.ModelSerializer):
        class Meta:
                model = Gobp
                fields = ('idd','term','goid','genelist')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class CancerlandingSerializer(serializers.ModelSerializer):
        class Meta:
                model = Cancerlanding
                fields = ('cancer','cancerLink','tool','netzoo','netzooLink','netzooRel','network','ppi','ppiLink','motif','expression','expLink','tfs','genes','refs','refs2','samples')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                return data

class DruglandingSerializer(serializers.ModelSerializer):
        class Meta:
                model  = Druglanding
                fields = ('number','drug','tool','netzoo','netzooRel','network','ppi','motif','expression','tfs','genes','ppiLink','refs','samples','expLink','nnets','druglink')

        def to_representation(self, instance):
                data = super().to_representation(instance)
                #data['is_on_sale'] = instance.is_on_sale()
                #data['current_price'] = instance.current_price()
                return data
