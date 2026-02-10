import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remdesk_project.settings')
django.setup()

from talenthub.models import TalentProfile, Service, CaseStudy

def verify_data():
    print("--- Production Database QA Check ---")
    
    # Check 1: Talent Pool
    talent_count = TalentProfile.objects.count()
    print(f"✅ Talent Profiles: {talent_count}")
    
    # Check 2: Services
    service_count = Service.objects.count()
    print(f"✅ Services: {service_count}")
    
    # Check 3: Case Studies
    case_study_count = CaseStudy.objects.count()
    print(f"✅ Case Studies: {case_study_count}")

    if talent_count > 0 and service_count > 0:
        print("\n[RESULT] Database Migration SUCCESSFUL. Data is present.")
    else:
        print("\n[RESULT] WARNING: Database appears empty. Seeding might be needed.")

if __name__ == '__main__':
    verify_data()
