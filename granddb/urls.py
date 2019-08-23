from django.conf.urls import url
from django.contrib import admin

from grandapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^about/' ,views.about, name='about'),
    url(r'^cell/' ,views.cell, name='cell'),
    url(r'^drugs/', views.drug, name='drugs')
    #url(r'^adoptions/(\d+)/', views.pet_detail, name='pet_detail'),
]
