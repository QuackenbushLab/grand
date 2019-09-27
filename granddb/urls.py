from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings

from grandapp import views,api_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^about/' ,views.about, name='about'),
    url(r'^cell/' ,views.cell, name='cell'),
    url(r'^drugs/', view=views.drug, name='drugs'),
    url(r'^tissues/', view=views.tissue, name='tissues'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^erroremail/', views.erroremail, name='erroremail'),
    url('api/v1/drugs/', api_views.DrugList.as_view()),
    path('api/v1/drugresultup/', api_views.DrugResultListUp.as_view()),
    path('api/v1/drugresultdown/', api_views.DrugResultListDown.as_view()),
    path('api/v1/disease/', api_views.DiseaseList.as_view()),
    path('api/v1/gwas/', api_views.GwasList.as_view()),
    path('analysis/', view=views.analysis, name='analysis'),
    path('disease/',view=views.disease, name='disease'),
    path('help/',view=views.help, name='help'),
    path('analysisexample/', view=views.analysisexample, name='analysisexample'),
    url(r'^diseaseexample/', view=views.diseaseexample, name='diseaseexample'),
    url(r'^drugresult/(\d+)/', view=views.drugresult, name='drugresult'),
    url(r'^diseaseresult/(\d+)', view=views.diseaseresult, name='diseaseresult'),
    path('api/v1/drugresultup/<int:id>/',  api_views.DrugRetrieveUpdateDestroyUp.as_view()),
    path('api/v1/drugresultdown/<int:id>/',  api_views.DrugRetrieveUpdateDestroyDown.as_view()),
    path('api/v1/params/<int:id>/',  api_views.ParamRetrieveUpdateDestroy.as_view()),
    path('api/v1/disease/<int:id>/',  api_views.DiseaseRetrieveUpdateDestroy.as_view()),
    path('api/v1/gwas/<int:id>/',  api_views.GwasRetrieveUpdateDestroy.as_view()),
]
