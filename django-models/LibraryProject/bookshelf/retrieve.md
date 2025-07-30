from bookshelf.models import Book

# Retrieve the book by its primary key (id)
# Assuming book1 was the first book created, its ID is likely 1
# You might need to adjust the ID if you've created multiple books or restarted the shell.
# A more robust way is to retrieve by title if it's unique, or by the object itself if still in memory.
try:
    retrieved_book = Book.objects.get(title="1984")
except Book.DoesNotExist:
    # If the title was updated to "Nineteen Eighty-Four" previously, retrieve by the new title
    retrieved_book = Book.objects.get(title="Nineteen Eighty-Four")

print(f"Title: {retrieved_book.title}")
print(f"Author: {retrieved_book.author}")
print(f"Publication Year: {retrieved_book.publication_year}")