from django.urls import path
from . import views

app_name = 'talenthub'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('talent-pool/', views.talent_pool, name='talent_pool'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('contact/', views.contact, name='contact'),
]
