from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Library, Author # Import Author as well

# Function-based View to list all books
def book_list_view(request):
    books = Book.objects.all().order_by('title') # Get all books, ordered by title
    context = {
        'books': books
    }
    return render(request, 'list_books.html', context)

# Class-based View to display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library' # The object will be available as 'library' in the template

    # Override get_context_data to add related books (though DetailView handles library.books.all directly)
    # This is more for complex scenarios, but good to know
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The 'library' object is already in context from DetailView
        # context['books_in_library'] = self.object.books.all()
        return context