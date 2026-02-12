from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('pricing/', views.pricing, name='pricing'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('careers/', views.careers, name='careers'),
    path('submit-lead/', views.submit_lead, name='submit_lead'),
    
    # Auth placeholders (or use Allauth URLs)
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    
    # Profile
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Renamed/Deprecated
    path('employers/', views.index, name='employers'), # Redirect to home for now, or keep if specific page needed
]
