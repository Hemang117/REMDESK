from django.db import models

class EmployerRequest(models.Model):
    ROLE_CHOICES = [
        ('Software Engineer', 'Software Engineer'),
        ('Product Manager', 'Product Manager'),
        ('Designer', 'Designer'),
        ('Sales/Marketing', 'Sales/Marketing'),
        ('Other', 'Other'),
    ]

    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    work_email = models.EmailField()
    role_to_hire = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} - {self.role_to_hire}"

class CandidateApplication(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    primary_skill = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    portfolio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.primary_skill}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
