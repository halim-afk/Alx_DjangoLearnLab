# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse # Import reverse for dynamic URLs
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post, Comment # Import Comment model
from .forms import CustomUserCreationForm, CustomUserChangeForm, PostForm, CommentForm # Import CommentForm
from django.contrib.auth import login as auth_login


# --- Authentication Views ---

def register(request):
    """
    Handles user registration.
    If POST request: validates and saves new user, then logs them in.
    If GET request: displays an empty registration form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # Automatically log in the user after successful registration
            messages.success(request, f'Welcome, {user.username}! Your registration was successful.')
            return redirect('profile') # Redirect to the user's profile page
        else:
            # Display form errors to the user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = CustomUserCreationForm() # Empty form for GET request
    return render(request, 'blog/register.html', {'form': form})

@login_required # Ensures only logged-in users can access this view
def profile(request):
    """
    Allows authenticated users to view and update their profile details.
    """
    if request.method == 'POST':
        # Populate form with submitted data and current user's instance
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile') # Redirect back to the profile page to show updated data
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field.replace('_', ' ').capitalize()}: {error}")
    else:
        # Populate form with current user's instance for GET request
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})


# --- Blog Post CRUD Views ---

class PostListView(ListView):
    """
    Displays a list of all blog posts, ordered by the latest published_date.
    This view is accessible to all users (public).
    """
    model = Post # Specifies the Django model to retrieve data from
    template_name = 'blog/post_list.html' # Path to the template file
    context_object_name = 'posts' # The name of the variable in the template that holds the queryset (list of posts)
    # Default ordering is set in Post.Meta, but can be overridden here if needed:
    # ordering = ['-published_date']
    # Optional: Enable pagination to display a limited number of posts per page
    paginate_by = 5

class PostDetailView(DetailView):
    """
    Displays the full content of a single blog post.
    This view is accessible to all users (public).
    """
    model = Post # Specifies the Django model to retrieve a single object from
    template_name = 'blog/post_detail.html' # Path to the template file

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create new blog posts.
    Requires the user to be logged in (`LoginRequiredMixin`).
    Automatically assigns the currently logged-in user as the author of the post.
    """
    model = Post # Specifies the model to create an instance of
    form_class = PostForm # Uses the PostForm for handling input fields (title, content)
    template_name = 'blog/post_form.html' # Reuses a generic form template for creation and update
    success_url = reverse_lazy('post_list') # Redirect to the 'post_list' page after successful creation

    def form_valid(self, form):
        """
        Overrides the default form_valid method to automatically set the 'author'
        field of the new Post instance to the currently logged-in user.
        """
        form.instance.author = self.request.user # Set the author of the post
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form) # Call the parent method to save the form instance

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the author of a post to update their own post.
    Requires user to be logged in (`LoginRequiredMixin`) and
    to be the actual author of the post (`UserPassesTestMixin`).
    """
    model = Post # Specifies the model to retrieve and update
    form_class = PostForm # Uses the PostForm for handling input fields
    template_name = 'blog/post_form.html' # Reuses the generic form template
    # success_url is automatically handled by the get_absolute_url method on the Post model

    def form_valid(self, form):
        """
        Ensures the author field remains unchanged during an update.
        """
        form.instance.author = self.request.user # Ensure author is still the current user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        """
        Tests if the currently logged-in user is the author of the post.
        This prevents unauthorized users from editing other people's posts.
        """
        post = self.get_object() # Get the specific Post object being accessed
        # Return True if the logged-in user matches the post's author, otherwise False
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the author of a post to delete their own post.
    Requires user to be logged in (`LoginRequiredMixin`) and
    to be the actual author of the post (`UserPassesTestMixin`).
    """
    model = Post # Specifies the model to delete
    template_name = 'blog/post_confirm_delete.html' # Template for deletion confirmation
    success_url = reverse_lazy('post_list') # Redirect to the 'post_list' page after successful deletion

    def test_func(self):
        """
        Tests if the currently logged-in user is the author of the post.
        This prevents unauthorized users from deleting other people's posts.
        """
        post = self.get_object() # Get the specific Post object being accessed
        # Return True if the logged-in user matches the post's author, otherwise False
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        """
        Overrides the default delete method to add a success message.
        """
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

# --- Comment CRUD Views (New) ---

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Allows authenticated users to create a new comment on a specific post.
    The post ID is passed in the URL (post_pk).
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html' # Use a separate template for comment creation/editing

    def form_valid(self, form):
        """
        Overrides form_valid to set the 'post' and 'author' fields of the comment
        before saving.
        """
        post = get_object_or_404(Post, pk=self.kwargs['post_pk']) # Get the Post object from URL kwargs
        form.instance.post = post # Link the comment to the correct post
        form.instance.author = self.request.user # Set the author to the logged-in user
        messages.success(self.request, 'Your comment has been posted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        """
        After successfully creating a comment, redirect back to the post's detail page.
        """
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_pk']})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows the author of a comment to edit their own comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        """
        Ensures the comment's author and post association remain unchanged.
        """
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        """
        Checks if the logged-in user is the author of the comment being updated.
        """
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        """
        After successfully updating a comment, redirect back to the post's detail page.
        """
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows the author of a comment to delete their own comment.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html' # Confirmation template for deletion

    def test_func(self):
        """
        Checks if the logged-in user is the author of the comment being deleted.
        """
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        """
        After successfully deleting a comment, redirect back to the post's detail page.
        """
        # Ensure 'self.object' is available before deletion is performed
        post_pk = self.get_object().post.pk
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return reverse('post_detail', kwargs={'pk': post_pk})
