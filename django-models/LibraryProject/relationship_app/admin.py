# relationship_app/admin.py
from django.contrib import admin
from .models import Author, Book, Library, Librarian # Import all your models

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)