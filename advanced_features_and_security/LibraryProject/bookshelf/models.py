from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password=None, **extra_fields):
        if not email:
            raise ValueError("يجب إدخال البريد الإلكتروني")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, date_of_birth, password, **extra_fields)

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
[15:53, 01/08/2025] Chatgpt: objects = CustomUserManager()

    def str(self):
        return self.username


class SomeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# Define the Book model
class Book(models.Model):
    """
    Represents a book in the library system.

    Attributes:
        title (CharField): The title of the book, with a maximum length of 200 characters.
        author (CharField): The author of the book, with a maximum length of 100 characters.
        publication_year (IntegerField): The year the book was published.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """
        Returns a string representation of the Book instance.
        This is useful for displaying the book in the Django admin and shell.
        """
        return f"{self.title} by {self.author} ({self.publication_year})"

    class Meta:
        """
        Meta options for the Book model.
        Defines verbose names and ordering for the model.
        """
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title'] # Order books by title by default
