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
            'resume': forms.FileInput(attrs={'class': 'form-input', 'accept': '.pdf,.doc,.docx'}),
        }

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.fields['resume'].required = True
        self.fields['resume'].help_text = 'Upload your resume (PDF or DOC, max 5MB)'

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'How can we help you?', 'class': 'form-textarea'}),
        }

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'current_role', 'experience_years', 'skills', 'linkedin_url', 'portfolio_url', 'resume', 'is_looking_for_job']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'current_role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Current Role (e.g. Senior Python dev)'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Years of Experience'}),
            'skills': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'List your top skills (comma separated)'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'LinkedIn Profile URL'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'Portfolio/GitHub URL'}),
            'resume': forms.FileInput(attrs={'class': 'form-input'}),
            'is_looking_for_job': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        if commit:
            profile.save()
            # Save User fields
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
        return profile
