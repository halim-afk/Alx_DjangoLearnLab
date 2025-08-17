

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Post # Import the Post model
from .models import Post, Comment
from taggit.forms import TagWidget() # NEW: Import TagWidget for better tag input styling


# Custom User Creation Form to include email (for registration)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'}) # Add basic styling class
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # Add email to the default fields
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            # password2 is handled by UserCreationForm implicitly
        }

# Custom User Change Form for profile editing
class CustomUserChangeForm(UserChangeForm):
    password = None # Remove password field from profile edit form for security and UX

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') # Fields editable by user
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Form for Post creation and update
class PostForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Post objects.
    Automatically handles validation and saving based on the Post model.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags'] # Fields that the user will input via the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post content here...', 'rows': 10}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags (e.g., python, django, webdev)'}), # NEW: Use TagWidget

        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']

# New: Form for Comment creation and update
class CommentForm(forms.ModelForm):
    """
    Form for creating and updating Comment objects.
    """
    class Meta:
        model = Comment
        fields = ['content'] # Only content is directly input by the user
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...', 'rows': 4}),
        }
