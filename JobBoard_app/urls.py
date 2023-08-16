from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Job related views
    path('job_listings/', views.job_listings, name='job_listings'),
    path('jobs_details/<int:job_id>/', views.job_detail, name='job_detail'),
    
    # Post a new job (anyone can post a job without logging in)
    path('add_job/', views.add_job_post, name='add_job_post'),

    #Outputs results for job title searches
    path('search-results/', views.job_search_results, name='job_search_results'),
    
    
    # Removed status update view since there's no authentication.
]

#Reference: 
#https://docs.djangoproject.com/en/3.2/topics/http/urls/
