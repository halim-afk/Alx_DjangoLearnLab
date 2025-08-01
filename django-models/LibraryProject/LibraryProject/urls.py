from django.contrib import admin
from django.urls import path, include
from .views import list_books, LibraryDetailView, edit_book, delete_book, add_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]
