from django import forms
from .models import JobPost, Comment

class JobPostForm(forms.ModelForm):
    """
    A form for creating and updating job posts.
    Each field has been enhanced with Bootstrap classes for styling.
    """
    
    title = forms.CharField(
        max_length=200, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'})
    )
    
    description = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Job Description'})
    )
    
    contact_email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'})
    )

    class Meta:
        model = JobPost
        fields = ['title', 'description', 'contact_email']


class CommentForm(forms.ModelForm):


    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : ''})
    )
    text = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : ''})
    )

    class Meta:
        model = Comment
        fields = ['name','text'] #name added here
    

# References:
# 1. Django ModelForms: https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
# 2. Styling Django forms with Bootstrap: https://django-crispy-forms.readthedocs.io/en/latest/
# 3. Django Forms documentation: https://docs.djangoproject.com/en/3.2/topics/forms/
