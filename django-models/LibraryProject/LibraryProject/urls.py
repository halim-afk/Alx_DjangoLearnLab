from django.contrib import admin
from django.urls import path, include
from relationship_app.views import list_books, LibraryDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),  # تشمل جميع روابط العلاقة
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
