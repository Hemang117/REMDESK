from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LeadForm, CandidateForm, ContactForm
from .models import Lead, RoleCategory, Service, Testimonial, TeamMember

def index(request):
    lead_form = LeadForm()
    testimonials = Testimonial.objects.all()[:3]
    role_categories = RoleCategory.objects.all()
    context = {
        'lead_form': lead_form,
        'testimonials': testimonials,
        'role_categories': role_categories,
    }
    return render(request, 'core/index.html', context)

def services(request):
    services_list = Service.objects.all()
    role_categories = RoleCategory.objects.all()
    context = {
        'services': services_list,
        'role_categories': role_categories,
    }
    return render(request, 'core/services.html', context)

def pricing(request):
    lead_form = LeadForm() # For modal or bottom CTA
    return render(request, 'core/pricing.html', {'lead_form': lead_form})

def how_it_works(request):
    lead_form = LeadForm()
    return render(request, 'core/how_it_works.html', {'lead_form': lead_form})

def about(request):
    team_members = TeamMember.objects.all()
    return render(request, 'core/about.html', {'team_members': team_members})

def contact(request):
    if request.method == 'POST':
        # Check if it's the contact form or lead form (if you reuse this view)
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent! We will translate this into action shortly.')
            return redirect('contact')
    else:
        # Default to LeadForm since the page acts as "Share Requirements" mostly
        # If you need both, you might need two separate forms in context or a toggle
        form = LeadForm()
    
    return render(request, 'core/contact.html', {'form': form})

def submit_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Requirement details received! Our talent specialists will contact you within 24 hours.')
            # Redirect to where they came from or a thank you page
            next_url = request.POST.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Please correct the errors in the form.')
            # ideally re-render the page with errors, but for now redirecting back
            return redirect(request.META.get('HTTP_REFERER', 'index'))
    return redirect('index')

def careers(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application submitted! We will be in touch.')
            return redirect('careers')
    else:
        form = CandidateForm()
    return render(request, 'core/careers.html', {'form': form})

# Login/Signup placeholders if used by Auth system, otherwise remove if handled by Allauth/standard
def login_page(request):
    return redirect('account_login')

def signup_page(request):
    return redirect('account_signup')
