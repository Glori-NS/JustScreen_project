from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Authentication related URLs
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),  # Using the CustomLoginView for authentication
    path('signup/', views.signup_view, name='signup'),

    # Dashboard views
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Redirects to appropriate dashboard depending on user type
    path('dashboard/candidate/', views.candidate_dashboard, name='candidate_dashboard'), 
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),

    # Job related views
    path('job_listings/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),

    # Application status update for recruiters
    path('applications/<int:application_id>/update_status/', views.update_application_status, name='update_application_status'),
]
#Reference: 
#https://docs.djangoproject.com/en/3.2/topics/http/urls/