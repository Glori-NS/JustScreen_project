from django.db import models
from django.contrib.auth.models import AbstractUser

# User Model 
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'recruiter'),
        (2, 'candidate'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

# Job Posting, Candidate and Application Models 
class JobPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)  # Optional: to tie job post to a recruiter

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Link candidate to user for authentication and profile
    name = models.CharField(max_length=100)
    contact_info = models.TextField()
    resume = models.FileField(upload_to='resumes/')

class Application(models.Model):
    APPLICATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default='pending')

