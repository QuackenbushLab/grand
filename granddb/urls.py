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
      contact=openapi.Contact(email="http://grand.networkmedicine.org/about/"),
      license=openapi.License(name="GPL License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^about/' ,views.about, name='about'),
    url(r'^cell/' ,views.cell, name='cell'),
    url('tissues/$', view=views.tissue, name='tissues'),
    url(r'-tissue/$', view=views.tissuelanding, name='tissuelanding'),
    url(r'-drug/$', view=views.druglanding, name='druglanding'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^erroremail/', views.erroremail, name='erroremail'),
    url('api/v1/drugs/', api_views.DrugList.as_view()),
    url('drugs/$', view=views.drug, name='drugs'),
    url('api/v1/drugresultup/', api_views.DrugResultListUp.as_view()),
    url('api/v1/drugresultdown/', api_views.DrugResultListDown.as_view()),
    url('api/v1/disease/', api_views.DiseaseList.as_view()),
    url('api/v1/gwas/', api_views.GwasList.as_view()),
    url('api/v1/drugapi/', api_views.DrugApiList.as_view()),
    url('api/v1/tissueapi/', api_views.TissueList.as_view()),
    url('api/v1/cellapi/', api_views.CellList.as_view()),
    url('api/v1/tissueex/', api_views.TissueExList.as_view()),
    url('api/v1/tissuetar/', api_views.TissueTarList.as_view()),
    url('analysis/', view=views.analysis, name='analysis'),
    url('disease/',view=views.disease, name='disease'),
    url('help/',view=views.help, name='help'),
    url('download/',view=views.download, name='download'),
    url('analysisexample/', view=views.analysisexample, name='analysisexample'),
    url('analysisexampletfs/', view=views.analysisexampletfs, name='analysisexampletfs'),
    url(r'^diseaseexample/', view=views.diseaseexample, name='diseaseexample'),
    url(r'^drugresult/(\d+)/', view=views.drugresult, name='drugresult'),
    url(r'^diseaseresult/(\d+)', view=views.diseaseresult, name='diseaseresult'),
    path('api/v1/drugresultup/<int:id>/',  api_views.DrugRetrieveUpdateDestroyUp.as_view()),
    path('api/v1/drugresultdown/<int:id>/',  api_views.DrugRetrieveUpdateDestroyDown.as_view()),
    path('api/v1/params/<int:id>/',  api_views.ParamRetrieveUpdateDestroy.as_view()),
    path('api/v1/disease/<int:id>/',  api_views.DiseaseRetrieveUpdateDestroy.as_view()),
    path('api/v1/gwas/<int:id>/',  api_views.GwasRetrieveUpdateDestroy.as_view()),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
