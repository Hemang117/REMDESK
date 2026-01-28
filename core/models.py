from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class CandidateApplication(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    primary_skill = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    portfolio_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application from {self.full_name}"

class Lead(models.Model):
    BUDGET_CHOICES = [
        ('$1k-$3k', '$1,000 - $3,000 / month'),
        ('$3k-$5k', '$3,000 - $5,000 / month'),
        ('$5k-$10k', '$5,000 - $10,000 / month'),
        ('$10k+', '$10,000+ / month')
    ]
    TIMELINE_CHOICES = [
        ('immediately', 'Immediately (ASAP)'),
        ('1_month', 'Within 1 month'),
        ('1_3_months', '1-3 months'),
        ('exploring', 'Just exploring')
    ]

    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    role_requirements = models.TextField(help_text='Describe the role, skills, and experience needed.')
    budget_range = models.CharField(max_length=50, choices=BUDGET_CHOICES, blank=True, help_text='Select your budget range')
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, blank=True, help_text='When do you need to hire?')
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Lead from {self.company_name}"

class RoleCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class e.g., 'fa-code'")

    class Meta:
        verbose_name_plural = 'Role Categories'

    def __str__(self):
        return self.name

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_role = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.client_name} - {self.company_name}"

class EmployeeReview(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='reviews/', blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name}"
