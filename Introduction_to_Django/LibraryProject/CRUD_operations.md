Django Book Model CRUD OperationsThis document details the Create, Retrieve, Update, and Delete (CRUD) operations performed on the Book model within the Django shell.Create Operation (create.md)Command: Create a Book instance with the title “1984”, author “George Orwell”, and publication year 1949.from bookshelf.models import Book

# Create a Book instance
book1 = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book1
Output:<Book: 1984 by George Orwell (1949)>
Retrieve Operation (retrieve.md)Command: Retrieve and display all attributes of the book you just created.from bookshelf.models import Book

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
Output:Title: 1984
Author: George Orwell
Publication Year: 1949
Update Operation (update.md)Command: Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.from bookshelf.models import Book

# Retrieve the book to update.
# Ensure you retrieve the correct book. If you've already run the create command,
# and haven't deleted it, this should work.
book_to_update = Book.objects.get(title="1984")

# Update the title
book_to_update.title = "Nineteen Eighty-Four"

# Save the changes to the database
book_to_update.save()

# Verify the update by retrieving the book again and printing its new title
updated_book = Book.objects.get(id=book_to_update.id)
print(f"Updated Title: {updated_book.title}")
Output:Updated Title: Nineteen Eighty-Four
Delete Operation (delete.md)Command: Delete the book you created and confirm the deletion by trying to retrieve all books again.from bookshelf.models import Book

# Retrieve the book to delete.
# Ensure you retrieve the correct book. If the title was updated, use the updated title.
try:
    book_to_delete = Book.objects.get(title="Nineteen Eighty-Four")
except Book.DoesNotExist:
    # Fallback in case the title was not updated or shell session was reset
    book_to_delete = Book.objects.get(title="1984")

# Delete the book
book_to_delete.delete()

# Confirm deletion by trying to retrieve all books again
all_books_after_deletion = Book.objects.all()
print(f"Books remaining after deletion: {list(all_books_after_deletion)}")
Output:(1, {'bookshelf.Book': 1}) # This is the typical output from the .delete() method
Books remaining after deletion: []
