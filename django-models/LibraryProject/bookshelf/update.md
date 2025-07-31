Command: Update the title of “1984” to “Nineteen Eighty-Four” and save the changes.from bookshelf.models import Book

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
