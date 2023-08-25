from django.db import models


#Removed the CustomUser model: 
#Since I'm removing user authentication, there's no need for a CustomUser model.

#JobPost Changes: 
#Removed the created_by foreign key because there's no longer a CustomUser model.

#Remove the Candidate and Application models: 
#If there's no user authentication, there's no need to track individual candidates or applications within the system.



# =========================
# Job Related Model
# =========================

class JobPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    company_name = models.CharField(max_length=200, blank=True, null=True)  
    # Name of the company posting the job
    
    contact_email = models.EmailField(max_length=255, blank=True, null=True)  
    # Email for job inquiries
    
    date_posted = models.DateTimeField(auto_now_add=True)  
    # Date when the job was posted

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

# =========================
# Comment Model
# =========================

class Comment(models.Model):
    JobPost = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='comments')

    name = models.CharField(max_length=255)
    # Users to add their names

    text = models.TextField()
    # Textbox for users to enter comments

    created_on = models.DateTimeField(auto_now_add=True)
    # Timestap when comments are created

    def __str__(self):
        return f" Comment by {self.name} on {self.created_on}"


#References: 
#https://docs.djangoproject.com/en/3.2/topics/db/models/
#https://docs.djangoproject.com/en/3.2/topics/auth/default/
#https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/ 