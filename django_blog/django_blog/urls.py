"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))s
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import UserLoginView, register ,profile ,UserLogoutView , user_logout, user_login
from django.views import ( # Import specific class-based views for clarity
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # include app urls
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    # --- Blog Post CRUD URLs ---
    # Home page: lists all blog posts
    path('', PostListView.as_view(), name='post_list'),
    # Create new post
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    # View a single post (uses primary key 'pk' to identify the post)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # Edit an existing post (uses primary key 'pk')
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    # Delete an existing post (uses primary key 'pk')
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
