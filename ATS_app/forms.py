from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
     class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type')
        labels= {
            'user_type': 'I am a ',
        }
