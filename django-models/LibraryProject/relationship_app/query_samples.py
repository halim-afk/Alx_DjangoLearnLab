from .models import Author, Book, Library, Librarian

Get all books by a specific author
def get_books_by_author(author_name):
    # This function retrieves all books written by a given author name
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

Get all books in a specific library
def get_books_in_library(library_name):
    # This function retrieves all books in the specified library
    library = Library.objects.get(name=library_name)
    return library.books.all()

Get the librarian of a specific library
def get_librarian_of_library(library_name):
    # This function retrieves the librarian assigned to the given library
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)