from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employers/', views.employers, name='employers'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
]
