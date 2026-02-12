from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LeadForm, CandidateForm, ContactForm, UserProfileForm
from .models import Lead, RoleCategory, Service, Testimonial, TeamMember

@login_required
def profile_dashboard(request):
    profile = request.user.profile
    
    # Calculate approximate profile completeness
    completeness = 0
    if profile.current_role: completeness += 20
    if profile.skills: completeness += 20
    if profile.experience_years > 0: completeness += 20
    if profile.resume: completeness += 20
    if profile.linkedin_url or profile.portfolio_url: completeness += 20
    
    # Determine progress ring color
    if completeness >= 80:
        ring_color = '#10B981'  # Green
    elif completeness >= 40:
        ring_color = '#F59E0B'  # Amber
    else:
        ring_color = '#EF4444'  # Red

    context = {
        'profile': profile,
        'completeness': completeness,
        'ring_color': ring_color,
    }
    return render(request, 'core/profile/dashboard.html', context)

@login_required
def profile_edit(request):
    profile = request.user.profile
    
    # ── Rate Limiting (DISABLED — uncomment to re-enable) ──────────────
    # from django.utils import timezone
    # from datetime import timedelta
    # now = timezone.now()
    # two_hours_ago = now - timedelta(hours=2)
    # five_mins_ago = now - timedelta(minutes=5)
    # if request.method == 'POST' and not request.user.is_superuser:
    #     if profile.updated_at > two_hours_ago and profile.created_at < five_mins_ago:
    #         next_update = profile.updated_at + timedelta(hours=2)
    #         remaining_minutes = int((next_update - now).total_seconds() / 60)
    #         messages.error(request, f"You can only update your profile once every 2 hours. Please try again in {remaining_minutes} minutes.")
    #         return redirect('profile_dashboard')
    # ─────────────────────────────────────────────────────────────────────

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            uploaded_file = request.FILES.get('resume')
            if uploaded_file:
                if uploaded_file.size > 5 * 1024 * 1024:
                    messages.error(request, "File too large. Please upload under 5MB.")
                    return render(request, 'core/profile/edit.html', {'form': form})
                
                # Email the resume to HR as well
                from django.core.mail import EmailMessage
                import os
                try:
                    admin_email = os.getenv('EMAIL_HOST_USER', 'admin@remdeskjobs.com')
                    email = EmailMessage(
                        subject=f"Updated Resume: {request.user.first_name} {request.user.last_name}",
                        body=f"User {request.user.username} updated their profile resume.\n\nSee attachment.",
                        from_email=None,
                        to=[admin_email],
                    )
                    email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
                    email.send()
                    # Reset file cursor so Cloudinary can re-read and upload it
                    uploaded_file.seek(0)
                    messages.info(request, "Resume sent to HR successfully!")
                except Exception as e:
                    print(f"Resume email failed: {e}")
                    # Reset file cursor even if email fails, so Cloudinary can still save
                    uploaded_file.seek(0)

            # Cloudinary handles file storage — no filesystem workaround needed
            form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_dashboard')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'core/profile/edit.html', {'form': form})

def careers(request):
    # Smart Redirect: If logged in, go to dashboard or edit profile
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            # If they are "looking for a job", maybe dashboard? 
            # Or if they have a profile, we assume they apply via profile/1-click later.
            # For now, let's redirect to dashboard to avoid duplicate "Guest" applications.
            return redirect('profile_dashboard')

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('resume')
            if uploaded_file:
                if uploaded_file.size > 5 * 1024 * 1024:
                    messages.error(request, "File too large. Please upload under 5MB.")
                    return render(request, 'core/careers.html', {'form': form})
            
            # Email the resume to HR
            if uploaded_file:
                from django.core.mail import EmailMessage
                import os
                
                try:
                    admin_email = os.getenv('EMAIL_HOST_USER', 'admin@remdeskjobs.com')
                    email = EmailMessage(
                        subject=f"New Resume: {form.cleaned_data['full_name']}",
                        body=f"A new candidate applied.\n\nName: {form.cleaned_data['full_name']}\nRole: {form.cleaned_data['primary_skill']}\nExperience: {form.cleaned_data['experience_years']} years\n\nSee attachment for resume.",
                        from_email=None, 
                        to=[admin_email], 
                    )
                    email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
                    email.send()
                    # Reset file cursor so Cloudinary can re-read and upload it
                    uploaded_file.seek(0)
                except Exception as e:
                    print(f"Resume email failed: {e}")
                    uploaded_file.seek(0)
            
            # Cloudinary handles file storage — no filesystem workaround needed
            form.save()
            
            messages.success(request, 'Application submitted! We will be in touch.')
            return redirect('careers')
    else:
        form = CandidateForm()
    return render(request, 'core/careers.html', {'form': form})

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
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            
            # Email notification to admin
            from django.core.mail import EmailMessage
            import os
            try:
                admin_email = os.getenv('EMAIL_HOST_USER', 'admin@remdeskjobs.com')
                email = EmailMessage(
                    subject=f"📩 New Contact Message from {contact_msg.name}",
                    body=(
                        f"New contact form submission:\n\n"
                        f"Name: {contact_msg.name}\n"
                        f"Email: {contact_msg.email}\n\n"
                        f"Message:\n{contact_msg.message}\n\n"
                        f"Submitted: {contact_msg.created_at}\n"
                        f"---\nReply directly to: {contact_msg.email}"
                    ),
                    from_email=None,
                    to=[admin_email],
                    reply_to=[contact_msg.email],
                )
                email.send()
            except Exception as e:
                print(f"Contact email notification failed: {e}")
            
            messages.success(request, 'Message sent! We will translate this into action shortly.')
            return redirect('contact')
    else:
        form = LeadForm()
    
    return render(request, 'core/contact.html', {'form': form})

def submit_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            # Email notification to admin
            from django.core.mail import EmailMessage
            import os
            try:
                admin_email = os.getenv('EMAIL_HOST_USER', 'admin@remdeskjobs.com')
                email = EmailMessage(
                    subject=f"🏢 New Hiring Lead: {lead.company_name}",
                    body=(
                        f"New employer lead received!\n\n"
                        f"Contact: {lead.name}\n"
                        f"Company: {lead.company_name}\n"
                        f"Email: {lead.email}\n\n"
                        f"Role Requirements:\n{lead.role_requirements}\n\n"
                        f"Budget: {lead.get_budget_range_display() or 'Not specified'}\n"
                        f"Timeline: {lead.get_timeline_display() or 'Not specified'}\n\n"
                        f"Submitted: {lead.created_at}\n"
                        f"---\nReply directly to: {lead.email}"
                    ),
                    from_email=None,
                    to=[admin_email],
                    reply_to=[lead.email],
                )
                email.send()
            except Exception as e:
                print(f"Lead email notification failed: {e}")
            
            messages.success(request, 'Requirement details received! Our talent specialists will contact you within 24 hours.')
            next_url = request.POST.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return redirect(request.META.get('HTTP_REFERER', 'index'))
    return redirect('index')

def careers(request):
    # Smart Redirect: If logged in, send them to their dashboard
    if request.user.is_authenticated:
        return redirect('profile_dashboard')

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('resume')
            if uploaded_file:
                if uploaded_file.size > 5 * 1024 * 1024:
                    messages.error(request, "File too large. Please upload under 5MB.")
                    return render(request, 'core/careers.html', {'form': form})
            
            # Email the resume to HR
            if uploaded_file:
                from django.core.mail import EmailMessage
                import os
                
                try:
                    admin_email = os.getenv('EMAIL_HOST_USER', 'admin@remdeskjobs.com')
                    email = EmailMessage(
                        subject=f"New Resume: {form.cleaned_data['full_name']}",
                        body=f"A new candidate applied.\n\nName: {form.cleaned_data['full_name']}\nRole: {form.cleaned_data['primary_skill']}\nExperience: {form.cleaned_data['experience_years']} years\n\nSee attachment for resume.",
                        from_email=None,
                        to=[admin_email], 
                    )
                    email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
                    email.send()
                    # Reset file cursor so Cloudinary can re-read and upload it
                    uploaded_file.seek(0)
                except Exception as e:
                    print(f"Resume email failed: {e}")
                    uploaded_file.seek(0)
            
            # Cloudinary handles file storage — no filesystem workaround needed
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
