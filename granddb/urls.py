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
      description="GRAND is a database of gene regulatory networks that integrates tissues, cells, and small molecules. It hosts webserver functionalities to perform cloud analytics on the networks.",
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
    url(r'^about/' ,views.about, name='about'),
    url(r'^cell/' ,views.cell, name='cell'),
    url('tissues/$', view=views.tissue, name='tissues'),
    url(r'^tissues/(\w+)/', view=views.tissuelanding, name='tissuelanding'),
    url(r'-drug/$', view=views.druglanding, name='druglanding'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^erroremail/', views.erroremail, name='erroremail'),
    url('api/v1/drugs/', api_views.DrugList.as_view()),
    url('drugs/$', view=views.drug, name='drugs'),
    url('api/v1/drugapi/', api_views.DruglandingList.as_view()),
    url('api/v1/tissueapi/', api_views.TissuelandingList.as_view()),
    url('api/v1/cellapi/', api_views.CellList.as_view()),
    url('analysis/', view=views.analysis, name='analysis'),
    url('disease/',view=views.disease, name='disease'),
    url('help/',view=views.help, name='help'),
    url('download/',view=views.download, name='download'),
    url('analysisexample/', view=views.analysisexample, name='analysisexample'),
    url('analysisexampletfs/', view=views.analysisexampletfs, name='analysisexampletfs'),
    url(r'^diseaseexample/', view=views.diseaseexample, name='diseaseexample'),
    url(r'^drugresult/(\d+)/reverse/', view=views.drugresult, name='drugresult'),
    url(r'^drugresult/(\d+)/similar/', view=views.drugresultsimilar, name='drugresultsimilar'),
    url(r'^diseaseresult/(\d+)/gwas/', view=views.diseasegwas, name='diseasegwas'),
    url(r'^diseaseresult/(\d+)/hpo/', view=views.diseasehpo, name='diseasehpo'),
    url(r'^diseaseresult/(\d+)/tissueex/', view=views.diseasetissueex, name='diseaseex'),
    url(r'^diseaseresult/(\d+)/tissuetar/', view=views.diseasetissuetar, name='diseasetar'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
