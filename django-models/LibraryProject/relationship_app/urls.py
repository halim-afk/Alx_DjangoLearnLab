from django.urls import path
from .views import list_books, LibraryDetailView # Make sure these are imported directly

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='book_list'), # Corrected line
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]