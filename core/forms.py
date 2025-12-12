from django import forms
from .models import EmployerRequest, CandidateApplication, ContactMessage

class EmployerForm(forms.ModelForm):
    class Meta:
        model = EmployerRequest
        fields = ['company_name', 'contact_person', 'work_email', 'role_to_hire']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Acme Inc.'}),
            'contact_person': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'work_email': forms.EmailInput(attrs={'placeholder': 'john@acme.com'}),
            'role_to_hire': forms.Select(),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = CandidateApplication
        fields = ['full_name', 'email', 'primary_skill', 'experience_years', 'portfolio_url']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Jane Smith'}),
            'email': forms.EmailInput(attrs={'placeholder': 'jane@example.com'}),
            'primary_skill': forms.TextInput(attrs={'placeholder': 'e.g. Python, React, Sales'}),
            'experience_years': forms.NumberInput(attrs={'placeholder': '3'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/...'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'message': forms.Textarea(attrs={'rows': 5}),
        }
