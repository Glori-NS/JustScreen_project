from django.test import TestCase
from django.urls import reverse
from JobBoard_app.models import JobPost, Comment

# Tests related to the JobPost model
class JobPostModelTests(TestCase):
    
    # Test case for creating a job post and validating the fields
    def test_create_job_post(self):
        """
        This test verifies if a job post can be successfully created 
        and if the fields are stored as expected.
        """
        job = JobPost.objects.create(
            title="Software Engineer",
            description="We are looking for a Software Engineer.",
            company_name="Tech Corp",
            contact_email="jobs@techcorp.com",
        )
        self.assertEqual(job.title, "Software Engineer")
        self.assertEqual(job.company_name, "Tech Corp")

    # Test case for checking the string representation of a job post
    def test_string_representation(self):
        """
        This test checks if the string representation of a job post
        matches the job title.
        """
        job = JobPost(title="Software Engineer")
        self.assertEqual(str(job), "Software Engineer")
    
    # Test case for creating a job post without an email
    def test_job_without_email(self):
        """
        This test checks if a job post can be created without an email,
        and if so, the email field should be None.
        """
        job = JobPost.objects.create(
            title="Software Engineer",
            description="We are looking for a Software Engineer."
        )
        self.assertIsNone(job.contact_email)

# Tests related to the Comment model
class CommentModelTests(TestCase):
    
    # Test case for creating a comment and validating the fields
    def test_create_comment(self):
        """
        This test checks if a comment can be successfully added to 
        a job post and if the fields are stored as expected.
        """
        job = JobPost.objects.create(title="Software Engineer", description="Job Description")
        comment = Comment.objects.create(
            JobPost=job,
            name="Jane",
            text="Nice job post."
        )
        self.assertEqual(comment.JobPost, job)
        self.assertEqual(comment.name, "Jane")
        
    # Test case for the string representation of a comment
    def test_comment_str(self):
        """
        This test checks if the string representation of a comment
        includes the comment author's name.
        """
        job = JobPost.objects.create(title="Software Engineer", description="Job Description")
        comment = Comment.objects.create(
            JobPost=job,
            name="Jane",
            text="Nice job post."
        )
        self.assertTrue("Comment by Jane" in str(comment))
        
    # Test case for adding multiple comments to a single job post
    def test_multiple_comments(self):
        """
        This test verifies if multiple comments can be added to 
        a single job post.
        """
        job = JobPost.objects.create(title="Data Scientist", description="Job Description")
        Comment.objects.create(JobPost=job, name="Alice", text="Great job!")
        Comment.objects.create(JobPost=job, name="Bob", text="Interesting job!")
        self.assertEqual(Comment.objects.filter(JobPost=job).count(), 2)

# Tests related to the views for job posts
class JobPostViewsTests(TestCase):
    
    # Test case for the job_listings view
    def test_job_listings_view(self):
        """
        This test checks if the job_listings view is accessible and returns a 200 status code.
        """
        response = self.client.get(reverse('job_listings'))
        self.assertEqual(response.status_code, 200)

    # Test case for accessing non-existent job details
    def test_empty_job_details_view(self):
        """
        This test checks if the job_detail view returns a 404 status code
        when a non-existing job ID is provided.
        """
        response = self.client.get(reverse('job_detail', args=(999,)))
        self.assertEqual(response.status_code, 404)

    # Test case for adding a new job post via the add_job_post view
    def test_add_job_post_view(self):
        """
        This test checks if a new job post can be created using the add_job_post view,
        and if the new job post is saved to the database.
        """
        new_job_data = {
            'title': 'New Job',
            'description': 'Job Description',
            'company_name': 'New Corp',
            'contact_email': 'jobs@newcorp.com'
        }
        response = self.client.post(reverse('add_job_post'), new_job_data)
        self.assertEqual(JobPost.objects.count(), 1)
        self.assertEqual(JobPost.objects.first().title, 'New Job')
        
    # Test case for checking if comments are displayed in job_detail view
    def test_job_with_comments_view(self):
        """
        This test checks if the comments associated with a job post
        are displayed in the job_detail view.
        """
        job = JobPost.objects.create(title="Software Engineer", description="Job Description")
        Comment.objects.create(JobPost=job, name="Alice", text="Great job!")
        response = self.client.get(reverse('job_detail', args=(job.id,)))
        self.assertContains(response, "Great job!")
        
    # Test case for adding an anonymous comment
    def test_anonymous_comment(self):
        """
        This test checks if an anonymous comment can be added
        to a job post via the job_detail view.
        """
        job = JobPost.objects.create(title="Software Engineer", description="Job Description")
        anonymous_comment_data = {'text': 'Nice job!'}
        response = self.client.post(reverse('job_detail', args=(job.id,)), anonymous_comment_data)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().name, 'Anonymous')
