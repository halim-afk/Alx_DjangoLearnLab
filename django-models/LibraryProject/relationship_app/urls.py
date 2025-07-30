from django.urls import path
from .views import list_books, LibraryDetailView

app_name = 'relationship_app' # Namespace for your app's URLs

urlpatterns = [
    path('books/', views.book_list_view, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]