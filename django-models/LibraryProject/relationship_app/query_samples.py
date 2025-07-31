from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
