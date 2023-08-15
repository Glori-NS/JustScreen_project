from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST, require_GET
from .models import JobPost, Application
from .forms import CustomUserCreationForm
from .decorators import recruiter_required, candidate_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):

    def get_success_url(self):
        if self.request.user.user_type == 1:  # Recruiter
            return reverse('recruiter_dashboard')
        elif self.request.user.user_type == 2:  # Candidate
            return reverse('candidate_dashboard')
        else:
            return reverse('home')  # default redirect if something goes wrong


@login_required
@candidate_required
def candidate_dashboard(request):
    applications = Application.objects.filter(candidate__user=request.user)
    context = {'applications': applications}
    return render(request, 'candidate_dashboard.html', context)


@login_required
@recruiter_required
def recruiter_dashboard(request):
    job_listings = JobPost.objects.filter(created_by=request.user)
    context = {'job_listings': job_listings}
    return render(request, 'recruiter_dashboard.html', context)


def home(request):
    return render(request, 'base.html')


def job_listings(request):
    jobs = JobPost.objects.all()
    return render(request, 'ats_app/job_listing.html', {'jobs': jobs})


@require_POST
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    if not Application.objects.filter(candidate=request.user, job_post=job).exists():
        Application.objects.create(candidate=request.user, job_post=job)
        messages.success(request, 'Successfully applied for the job!')
    else:
        messages.warning(request, 'You have already applied for this job.')
    return redirect('job_listings')


def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'ats_app/job_detail.html', {'job': job})


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup_template.html', {'form': form})


@login_required
@recruiter_required
@require_POST
def add_job_post(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    job_post = JobPost(title=title, description=description, created_by=request.user)
    job_post.save()
    messages.success(request, "Job post added successfully!")
    return redirect('recruiter_dashboard')


@login_required
@recruiter_required
def review_applications(request, job_id):
    job = get_object_or_404(JobPost, id=job_id, created_by=request.user) 
    applications = Application.objects.filter(job_post=job)
    context = {'job': job, 'applications': applications}
    return render(request, 'review_applications.html', context)


@require_POST
@login_required
@recruiter_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if application.job_post.created_by != request.user:
        messages.error(request, 'Unauthorized action.')
        return redirect('recruiter_dashboard')

    new_status = request.POST.get('status')
    if new_status in ['pending', 'accepted', 'rejected']:
        application.status = new_status
        application.save()
        messages.success(request, 'Application status updated!')
    else:
        messages.error(request, 'Invalid application status.')

    return redirect(reverse('review_applications', args=[application.job_post.id]))
