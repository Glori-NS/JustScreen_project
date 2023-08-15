from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# Custom User Model
# =========================
class CustomUser(AbstractUser):
    RECRUITER = 'recruiter'
    CANDIDATE = 'candidate'
    
    USER_TYPE_CHOICES = (
        (RECRUITER, 'Recruiter'),
        (CANDIDATE, 'Candidate'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

# =========================
# Job Related Models
# =========================
class JobPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='job_posts')  

class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate_profile')  # Link candidate to user
    contact_info = models.TextField()
    resume = models.FileField(upload_to='resumes/')

class Application(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    APPLICATION_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=APPLICATION_STATUS_CHOICES, default=PENDING)

#References: 
#https://docs.djangoproject.com/en/3.2/topics/db/models/
#https://docs.djangoproject.com/en/3.2/topics/auth/default/
#https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/ 