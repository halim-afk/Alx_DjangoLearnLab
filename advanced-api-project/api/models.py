from django.db import models

# Represents an author who can have multiple books.
class Author(models.Model):
    name = models.CharField(max_length=255)  # Stores author's name.

    def __str__(self):
        return self.name


# Represents a book with a title, year, and linked author.
class Book(models.Model):
    title = models.CharField(max_length=255)  # Book title.
    publication_year = models.IntegerField()  # Year of publication.
    author = models.ForeignKey(
        Author,
        related_name="books",  # Allows reverse relation: author.books.all()
        on_delete=models.CASCADE  # Deletes books if the author is deleted.
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"


# Create your models here.
