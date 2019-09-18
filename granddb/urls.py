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
    path('api/v1/drugresult/', api_views.DrugResultList.as_view()),
    url(r'^analysis/', view=views.analysis, name='analysis'),
    path('drugresult/', view=views.drugresult, name='drugresult'),
    path('api/v1/drugresult/<int:id>/',  api_views.DrugRetrieveUpdateDestroy.as_view())
]
