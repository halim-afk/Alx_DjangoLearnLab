from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book, Author # Import Author as well
from .models import Library

# Function-based View to list all books
def list_books(request):
    books = Book.objects.all().order_by('title')
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)
# Class-based View to display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html' # <--- Corrected
    context_object_name = 'library'

    # Override get_context_data to add related books (though DetailView handles library.books.all directly)
    # This is more for complex scenarios, but good to know
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The 'library' object is already in context from DetailView
        # context['books_in_library'] = self.object.books.all()
        return context