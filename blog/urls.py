from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('lista_postow/', views.lista_postow, name='posty'),
]