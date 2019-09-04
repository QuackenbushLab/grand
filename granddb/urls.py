from django.conf.urls import url
from django.contrib import admin

from grandapp import views
import grandapp.api_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^about/' ,views.about, name='about'),
    url(r'^cell/' ,views.cell, name='cell'),
    url(r'^drugs/', view=views.drug, name='drugs'),
    url(r'^tissues/', view=views.tissue, name='tissues'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^erroremail/', views.erroremail, name='erroremail'),
    url('api/v1/drugs/', grandapp.api_views.DrugList.as_view()),
    #url(r'^adoptions/(\d+)/', views.pet_detail, name='pet_detail'),
]
