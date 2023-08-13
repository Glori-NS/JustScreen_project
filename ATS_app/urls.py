from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job_listings/', views.job_listings, name='job_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('signup/', views.signup_view, name='signup'),

]
