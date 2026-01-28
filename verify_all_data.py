import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remdesk_project.settings')
django.setup()

from core.models import ContactMessage, EmployerRequest, CandidateApplication

print("----------------------------------------------------------------")
print("📊 DATABASE REPORT")
print("----------------------------------------------------------------")

# 1. Contact Messages
msgs = ContactMessage.objects.all()
print(f"\n📨 CONTACT MESSAGES ({msgs.count()} found):")
for m in msgs:
    print(f"   - [{m.created_at.strftime('%Y-%m-%d %H:%M')}] {m.name}: {m.message[:50]}...")

# 2. Employer Requests
reqs = EmployerRequest.objects.all()
print(f"\n💼 EMPLOYER REQUESTS ({reqs.count()} found):")
for r in reqs:
    print(f"   - {r.company_name} wants a {r.role_to_hire} (Contact: {r.contact_person})")

# 3. Candidates
cands = CandidateApplication.objects.all()
print(f"\n👨‍💻 CANDIDATE APPLICATIONS ({cands.count()} found):")
for c in cands:
    print(f"   - {c.full_name} ({c.primary_skill}) - {c.experience_years} years exp")

print("\n----------------------------------------------------------------")
print("✅ SYSTEM STATUS: ONLINE & RECORDING")
print("----------------------------------------------------------------")
