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
    url(r'^analysis/', view=views.analysis, name='analysis'),
    url(r'^analysisexample/', view=views.analysisexample, name='analysisexample'),
    path('drugresult/', view=views.drugresult, name='drugresult'),
    path('api/v1/drugresultup/<int:id>/',  api_views.DrugRetrieveUpdateDestroyUp.as_view()),
    path('api/v1/drugresultdown/<int:id>/',  api_views.DrugRetrieveUpdateDestroyDown.as_view()),
    path('api/v1/params/<int:id>/',  api_views.ParamRetrieveUpdateDestroy.as_view()),
]
