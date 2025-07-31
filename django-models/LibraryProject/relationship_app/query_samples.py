from relationship_app.models import Author, Book, Library, Librarian
from .models import Author, Book, Library, Librarian

#Get all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)  # <- هذا السطر مطلوب للفحص
    return Book.objects.filter(author=author)      # <- وهذا أيضاً

#Get all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

#Retrieve the librarian for a library
def get_librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)  # <- مطلوب أيضاً
    return Librarian.objects.get(library=library)     # <- وهذا كذلك


def books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
