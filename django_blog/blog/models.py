from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # Used for get_absolute_url




# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=280, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Profile({self.user.username})'




# New: Comment Model
class Comment(models.Model):
    """
    Represents a comment on a blog post.
    """
    # ForeignKey to Post: A comment belongs to one post. If post is deleted, its comments are also deleted.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # ForeignKey to User: A comment is written by one user. If user is deleted, their comments are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order comments by creation date, oldest first, for chronological display
        ordering = ['created_at']

    def __str__(self):
        # Display a snippet of the comment content
        return f'Comment by {self.author.username} on "{self.post.title}"'

    def get_absolute_url(self):
        # Redirect back to the post detail page after comment creation/update/deletion
        return reverse('post_detail', kwargs={'pk': self.post.pk})




