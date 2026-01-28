import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remdesk_project.settings')
django.setup()

from talenthub.models import Service, TalentProfile, CaseStudy

def populate():
    # Services
    services_data = [
        {
            "title": "Tech Recruitment",
            "slug": "tech-recruitment",
            "short_description": "Hire top 1% developers in Python, React, Node.js.",
            "full_description": "Our AI-driven vetting process ensures you get world-class developers who communicate effectively and deliver on time. We specialize in Python, JavaScript, and Cloud technologies.",
            "icon_class": "fas fa-code",
            "price_starter": 1500,
            "price_pro": 3500
        },
        {
            "title": "Vehicle Testing & Validation",
            "slug": "vehicle-testing",
            "short_description": "Experts in CAN, UDS, and ADAS validation.",
            "full_description": " Specialized automotive engineers for HIL/SIL testing, protocol validation (CAN, LIN, UDS), and ADAS data collection.",
            "icon_class": "fas fa-car",
            "price_starter": 2000,
            "price_pro": 4500
        },
        {
            "title": "HR Optimization",
            "slug": "hr-optimization",
            "short_description": "Streamline your recruitment process.",
            "full_description": "End-to-end RPO services, employer branding, and payroll management for global teams.",
            "icon_class": "fas fa-users-cog",
            "price_starter": 1000,
            "price_pro": 2500
        }
    ]

    for s in services_data:
        Service.objects.get_or_create(slug=s['slug'], defaults=s)
    
    print("Services populated.")

    # Talent Profiles
    talents_data = [
        {
            "name": "Arjun Mehta",
            "role": "Senior Python Developer",
            "skills": "Python, Django, AWS, React",
            "location": "Bangalore, India",
            "experience_years": 8,
            "bio": "Full-stack developer with 8 years of experience building scalable SaaS platforms. Ex-Amazon.",
            "hourly_rate": 45.00
        },
        {
            "name": "Sarah Jenkins",
            "role": "Vehicle Validation Engineer",
            "skills": "CANoe, HIL, UDS, ADAS",
            "location": "Pune, India",
            "experience_years": 6,
            "bio": "Automotive engineer specialized in ADAS validation and HIL testing setups.",
            "hourly_rate": 55.00
        },
         {
            "name": "Vikram Singh",
            "role": "AI/ML Engineer",
            "skills": "PyTorch, TensorFlow, CV, NLP",
            "location": "Gurugram, India",
            "experience_years": 5,
            "bio": "Deep Learning expert focused on Computer Vision for autonomous driving.",
            "hourly_rate": 60.00
        }
    ]

    for t in talents_data:
        TalentProfile.objects.get_or_create(name=t['name'], defaults=t)

    print("Talents populated.")

    # Case Studies
    cases_data = [
        {
            "client_name": "DriveEasy Auto",
            "title": "Reduced HIL Testing Time by 40%",
            "summary": "How we deployed a team of 5 specialized validation engineers to speed up deployment.",
            "result_metric": "40% Faster Time-to-Market",
            "full_content": "Full story here...",
        },
        {
             "client_name": "FinTech Corp",
            "title": "Scaled Python Team from 0 to 20",
            "summary": "Built a complete backend team in 3 weeks for a Series B startup.",
            "result_metric": "Saved $1.2M/year",
            "full_content": "Full story here...",
        }
    ]

    for c in cases_data:
        CaseStudy.objects.get_or_create(title=c['title'], defaults=c)

    print("Case Studies populated.")

if __name__ == '__main__':
    populate()
