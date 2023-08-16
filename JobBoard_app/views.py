from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import JobPost
from django.contrib import messages


from django.contrib import messages

#1. Removed authentication related views
#2. Adjusted views related to 'JobPost' to
#reflect the removal of 'created_by' field.
#3. Removed views related to CustomUsers including Candidates and their applications



def home(request):
    """The main homepage view."""
    return render(request, 'base.html')

def job_listings(request):
    """Displays all available job listings."""
    jobs = JobPost.objects.all()
    return render(request, 'ats_app/job_listing.html', {'jobs': jobs})


def job_detail(request, job_id):
    """Displays detailed information about a specific job."""
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'ats_app/job_detail.html', {'job': job})

@require_POST
def add_job_post(request):
    """Allows any user to post new job listings."""
    title = request.POST.get('title')
    description = request.POST.get('description')
    company_name = request.POST.get('company_name')
    contact_email = request.POST.get('contact_email')
    
    job_post = JobPost(title=title, description=description, company_name=company_name, contact_email=contact_email)
    job_post.save()
    messages.success(request, "Job post added successfully!")
    
    return redirect('job_listings')

def job_search_results(request):
    job_title = request.GET.get('job_title', '')
    jobs = JobPost.objects.filter(title__icontains=job_title)
    
    return render(request, 'job_search_results_page.html', {'jobs': jobs, 'job_title': job_title})




#References:
#https://www.w3schools.com/django/django_views.php 
#https://realpython.com/tutorials/django/
#https://tutorial.djangogirls.org/en/ 
