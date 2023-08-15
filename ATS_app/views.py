from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST, require_GET
from .models import JobPost, Application, Candidate, CustomUser
from .forms import CustomUserCreationForm
from .decorators import recruiter_required, candidate_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    """Handles custom redirection after login based on user type."""

    def get_success_url(self):
        if self.request.user.user_type == 1:  # Recruiter
            return reverse('recruiter_dashboard')
        elif self.request.user.user_type == 2:  # Candidate
            return reverse('candidate_dashboard')
        else:
             return reverse('home')  # default redirect if something goes wrong

def user_dashboard(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('registration/login.html')  # Redirect to login page or view name

    # Check user type and redirect accordingly
    if request.user.user_type == 'RECRUITER':
        return redirect('recruiter_dashboard.html')  # Redirect to the recruiter's dashboard

    elif request.user.user_type == 'CANDIDATE':
        return redirect('candidate_dashboard.html')  # Redirect to the candidate's dashboard

    # Handle other user types or a default case
    else:
        return redirect('ats_app/user_dashboard.html')  # Redirect to a default dashboard or error page



@login_required
@candidate_required
def candidate_dashboard(request):
    """Displays the dashboard for candidates, showing their applications."""
    
    candidate = Candidate.objects.get(user=request.user)
    applications = Application.objects.filter(candidate=candidate)
    context = {'applications': applications}
    return render(request, 'Templates/candidate_dashboard.html', context)


@login_required
@recruiter_required
def recruiter_dashboard(request):
    """Displays the dashboard for recruiters, showing their job postings."""
    
    job_listings = JobPost.objects.filter(created_by=request.user)
    context = {'job_listings': job_listings}
    return render(request, 'Templates/recruiter_dashboard.html', context)


def home(request):
    """The main homepage view."""
    
    return render(request, 'base.html')


def job_listings(request):
    """Displays all available job listings."""
    
    jobs = JobPost.objects.all()
    return render(request, 'ats_app/job_listing.html', {'jobs': jobs})


@require_POST
@login_required
@candidate_required
def apply_for_job(request, job_id):
    """Allows a candidate to apply for a job."""
    
    job = get_object_or_404(JobPost, pk=job_id)
    candidate = Candidate.objects.get(user=request.user)
    if not Application.objects.filter(candidate=candidate, job_post=job).exists():
        Application.objects.create(candidate=candidate, job_post=job)
        messages.success(request, 'Successfully applied for the job!')
    else:
        messages.warning(request, 'You have already applied for this job.')
    return redirect('job_listings')


def job_detail(request, job_id):
    """Displays detailed information about a specific job."""
    
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'ats_app/job_detail.html', {'job': job})


def signup_view(request):
    """Handles user signup."""
    
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
    """Allows recruiters to post new job listings."""
    
    title = request.POST.get('title')
    description = request.POST.get('description')
    job_post = JobPost(title=title, description=description, created_by=request.user)
    job_post.save()
    messages.success(request, "Job post added successfully!")
    return redirect('recruiter_dashboard')


@login_required
@recruiter_required
def review_applications(request, job_id):
    """Allows recruiters to review applications for a specific job."""
    
    job = get_object_or_404(JobPost, id=job_id, created_by=request.user) 
    applications = Application.objects.filter(job_post=job)
    context = {'job': job, 'applications': applications}
    return render(request, 'review_applications.html', context)


@require_POST
@login_required
@recruiter_required
def update_application_status(request, application_id):
    """Allows recruiters to update the status of an application."""
    
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



#References:
#https://www.w3schools.com/django/django_views.php 
#https://realpython.com/tutorials/django/
#https://tutorial.djangogirls.org/en/ 
