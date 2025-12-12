from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmployerForm, CandidateForm, ContactForm

def index(request):
    return render(request, 'core/index.html')

def employers(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('employers')
    else:
        form = EmployerForm()
    return render(request, 'core/employers.html', {'form': form})

def careers(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application submitted! We will be in touch.')
            return redirect('careers')
    else:
        form = CandidateForm()
    return render(request, 'core/careers.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})

