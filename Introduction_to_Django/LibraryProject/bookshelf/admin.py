from django.contrib import admin
from .models import Book # Import your Book model

# Define the custom admin class for the Book model
class BookAdmin(admin.ModelAdmin):
    """
    Customizes the display and functionality of the Book model
    in the Django admin interface.
    """
    # 1. Display specific fields in the list view
    # This tuple defines which fields will be shown as columns in the list of books
    list_display = ('title', 'author', 'publication_year')

    # 2. Configure list filters
    # This tuple defines fields that can be used to filter the list of books
    # in the right sidebar of the admin change list page.
    list_filter = ('publication_year', 'author')

    # 3. Configure search capabilities
    # This tuple defines fields that will be searched when using the search bar
    # at the top of the admin change list page.
    # 'title__icontains' allows case-insensitive searching on the title.
    search_fields = ('title', 'author')

    # Optional: Add a fieldset for better organization on the add/change form
    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'author', 'publication_year')
    #     }),
    # )

# Register the Book model with the custom admin class
admin.site.register(Book, BookAdmin)
