from django.contrib import admin
from .models import EmployerRequest, CandidateApplication, ContactMessage

admin.site.register(EmployerRequest)
admin.site.register(CandidateApplication)
admin.site.register(ContactMessage)
