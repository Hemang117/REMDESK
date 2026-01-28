from django import forms
from .models import Lead, CandidateApplication, ContactMessage

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['company_name', 'name', 'email', 'role_requirements', 'budget_range', 'timeline']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name', 'class': 'form-input'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Work Email', 'class': 'form-input'}),
            'role_requirements': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the role, skills, and experience needed...', 'class': 'form-textarea'}),
            'budget_range': forms.Select(attrs={'class': 'form-input'}),
            'timeline': forms.Select(attrs={'class': 'form-input'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = CandidateApplication
        fields = ['full_name', 'email', 'primary_skill', 'experience_years', 'portfolio_url', 'linkedin_url', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-input'}),
            'primary_skill': forms.TextInput(attrs={'placeholder': 'Primary Skill (e.g., Python/Django)', 'class': 'form-input'}),
            'experience_years': forms.NumberInput(attrs={'placeholder': 'Years of Experience', 'class': 'form-input'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'Portfolio/GitHub URL', 'class': 'form-input'}),
            'linkedin_url': forms.URLInput(attrs={'placeholder': 'LinkedIn URL', 'class': 'form-input'}),
            'resume': forms.FileInput(attrs={'class': 'form-input'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'How can we help you?', 'class': 'form-textarea'}),
        }
