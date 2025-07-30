Command: Delete the book you created and confirm the deletion by trying to retrieve all books again.from bookshelf.models import Book

# Retrieve the book to delete.
# Ensure you retrieve the correct book. If the title was updated, use the updated title.
try:
    book = Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    # Fallback in case the title was not updated or shell session was reset
    book = Book.objects.get(title="1984")

# Delete the book
book.delete()

# Confirm deletion by trying to retrieve all books again
all_books_after_deletion = Book.objects.all()
print(f"Books remaining after deletion: {list(all_books_after_deletion)}")
Output:(1, {'bookshelf.Book': 1}) # This is the typical output from the .delete() method
Books remaining after deletion: []
