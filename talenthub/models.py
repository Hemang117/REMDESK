from django.db import models

class TalentProfile(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)  # e.g. Python Developer, CAN Expert
    skills = models.CharField(max_length=500, help_text="Comma-separated skills")
    location = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    bio = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='talent_images/', null=True, blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    icon_class = models.CharField(max_length=100, help_text="CSS class for icon (e.g., 'fas fa-code')")
    price_starter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_pro = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class CaseStudy(models.Model):
    client_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    result_metric = models.CharField(max_length=100, help_text="e.g., 'Reduced Recruitment Time by 80%'")
    full_content = models.TextField()
    image = models.ImageField(upload_to='case_study_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team_images/', null=True, blank=True)

    def __str__(self):
        return self.name
