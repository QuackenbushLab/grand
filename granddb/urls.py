from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from grandapp import views,api_views

schema_view = get_schema_view(
   openapi.Info(
      title="GRAND API",
      default_version='v1',
      description="GRAND is a database of gene regulatory networks that integrates tissues, cancer, cells, and small molecules. It hosts webserver functionalities to perform cloud analytics on the networks.",
      terms_of_service="https://creativecommons.org/licenses/by-sa/4.0/",
      contact=openapi.Contact(email="https://grand.networkmedicine.org/about/"),
      license=openapi.License(name="GPL License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

#please keep order
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^aviator_api/' ,views.aviator_api, name='aviator_api'),
    url(r'^about/' ,views.about, name='about'),
    url('cell/$' ,views.cell, name='cell'),
    url(r'^cell/(\w+)/', view=views.celllanding, name='celllanding'),
    url(r'genes/' ,views.genes, name='genes'),
    url(r'pathways/' ,views.pathways, name='pathways'),
    url(r'gwascatalog/' ,views.gwascatalog, name='gwascatalog'),
    url('cancers/$', view=views.cancer, name='cancers'),
    url(r'^cancers/(\w+)/', view=views.cancerlanding, name='cancerlanding'),
    url('tissues/$', view=views.tissue, name='tissues'),
    url(r'^tissues/(\w+)/', view=views.tissuelanding, name='tissuelanding'),
    url(r'_drug/$', view=views.druglanding, name='druglanding'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^cclemap/', views.babelomic, name='babelomic'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^ownnet/(\w+)/', views.ownnet, name='ownnet'),
    url(r'^netcomp/aggregate/(\w+)/', views.netcomp, name='netcomp'),
    url(r'^ownnetar/(\w+)/', views.owntaragg, name='owntaragg'),
    url(r'^erroremail/', views.erroremail, name='erroremail'),
    url(r'networks/aggregate/(\w+)/', view=views.networksagg, name='networksagg'),
    url(r'netcomp/targeting/(\w+)/', view=views.difftaragg, name='difftaragg'),
    url(r'networks/targeting/(\w+)/', view=views.taragg, name='taragg'),
    url(r'networks/drugtarg/(\w+)/', view=views.drugtarg, name='drugtarg'),
    url(r'networks/cluesbmit/(\w+)/', view=views.cluesubmit, name='cluesubmit'),
    url('drugs/$', view=views.drug, name='drugs'),
    url('api/v1/drugapi/', api_views.DruglandingList.as_view()),
    url('api/v1/tissueapi/', api_views.TissuelandingList.as_view()),
    url('api/v1/cancerapi/', api_views.CancerlandingList.as_view()),
    url('api/v1/geneapi/', api_views.GenelandingList.as_view()),
    url('api/v1/pathwayapi/', api_views.GobplandingList.as_view()),
    url('api/v1/gwasapi/', api_views.GwaslandingList.as_view()),
    url('analysis/', view=views.analysis, name='analysis'),
    url('disease/',view=views.disease, name='disease'),
    url('help/',view=views.help, name='help'),
    url('download/',view=views.download, name='download'),
    url('downloads/',view=views.downloads, name='downloads'),
    url(r'^drugresult/(\d+)/reverse/', view=views.drugresult, name='drugresult'),
    url(r'^drugresult/(\d+)/similar/', view=views.drugresultsimilar, name='drugresultsimilar'),
    url(r'^diseaseresult/(\d+)/gwas/', view=views.diseasegwas, name='diseasegwas'),
    url(r'^diseaseresult/(\d+)/hpo/', view=views.diseasehpo, name='diseasehpo'),
    url(r'^diseaseresult/(\d+)/tissueex/', view=views.diseasetissueex, name='diseaseex'),
    url(r'^diseaseresult/(\d+)/tissuetar/', view=views.diseasetissuetar, name='diseasetar'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
