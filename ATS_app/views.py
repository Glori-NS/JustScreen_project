from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import JobPost, Application

def home(request):
    return render(request, 'base.html')

def job_listings(request):
    jobs = JobPost.objects.all()
    return render(request, 'job_listing.html', {'jobs': jobs})

def apply_for_job(request, job_id):
    if request.user.is_authenticated:
        job = get_object_or_404(JobPost, pk=job_id)  # This will handle the case when the job doesn't exist
        if not Application.objects.filter(candidate=request.user, job_post=job).exists():
            Application.objects.create(candidate=request.user, job_post=job)
            messages.success(request, 'Successfully applied for the job!')
        else:
            messages.warning(request, 'You have already applied for this job.')
        return redirect('job_listings')
    else:
        messages.warning(request, 'Please login to apply for a job.')
        return redirect('login')  # redirect to the login page if the user is not authenticated

def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_detail.html', {'job': job})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # This will create a new User instance and save it to the database.
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup_template.html', {'form': form})


# Reference: Django official documentation on render().
# https://docs.djangoproject.com/en/3.1/topics/http/shortcuts/#render
