import os
import sys
import django

# Add your Django project's root directory to the Python path
# The project root is the directory containing manage.py and the main settings folder (e.g., LibraryProject)
# Since query_samples.py is in 'relationship_app', going up one level (..) gets us to 'LibraryProject'
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Corrected line!
sys.path.insert(0, PROJECT_ROOT)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# ... rest of your script

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    print("--- Creating Sample Data ---")

    # Create Authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    author3 = Author.objects.create(name="Harper Lee")

    # Create Books
    book1 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author1)
    book2 = Book.objects.create(title="1984", author=author2)
    book3 = Book.objects.create(title="To Kill a Mockingbird", author=author3)
    book4 = Book.objects.create(title="Animal Farm", author=author2)
    book5 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)

    # Create Libraries
    library1 = Library.objects.create(name="Central City Library")
    library2 = Library.objects.create(name="University Library")

    # Add books to libraries
    library1.books.add(book1, book2, book3)
    library2.books.add(book2, book4, book5)

    # Create Librarians
    librarian1 = Librarian.objects.create(name="Alice Smith", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Johnson", library=library2)

    print("\n--- Sample Queries ---")

    # Query all books by a specific author
    print("\nQuery all books by J.K. Rowling:")
    jk_rowling = Author.objects.get(name="J.K. Rowling")
    books_by_jk_rowling = Book.objects.filter(author=jk_rowling)
    for book in books_by_jk_rowling:
        print(f"- {book.title}")

    # List all books in a library
    print("\nList all books in Central City Library:")
    central_library = Library.objects.get(name="Central City Library")
    books_in_central_library = central_library.books.all()
    for book in books_in_central_library:
        print(f"- {book.title}")

    # Retrieve the librarian for a library
    print("\nRetrieve the librarian for University Library:")
    university_library = Library.objects.get(name="University Library")
    university_librarian = university_library.librarian
    print(f"- The librarian for {university_library.name} is {university_librarian.name}")

if __name__ == "__main__":
    run_queries()