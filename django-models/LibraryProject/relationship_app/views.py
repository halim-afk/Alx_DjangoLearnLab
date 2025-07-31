from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView  # Import class-based detail view
from .models import Library  # Import the Library model



def list_books(request):
    books = Book.objects.all()  # Get all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})  # Render the book list template

class LibraryDetailView(DetailView):
    model = Library  # Use the Library model
    template_name = 'relationship_app/library_detail.html'  # Template to render
    context_object_name = 'library'  # Name used in the template to refer to the object
