from django.shortcuts import render
from .models import TalentProfile, Service, CaseStudy, BlogPost

def index(request):
    services = Service.objects.all()[:6]
    case_studies = CaseStudy.objects.all()[:3]
    return render(request, 'talenthub/index.html', {
        'services': services,
        'case_studies': case_studies
    })

def services(request):
    services = Service.objects.all()
    return render(request, 'talenthub/services.html', {'services': services})

def talent_pool(request):
    talents = TalentProfile.objects.all()
    # Filter logic could go here
    return render(request, 'talenthub/talent_pool.html', {'talents': talents})

def case_studies(request):
    cases = CaseStudy.objects.all()
    return render(request, 'talenthub/case_studies.html', {'cases': cases})

def contact(request):
    return render(request, 'talenthub/contact.html')
