from django.urls import path
from .views import UserLoginView, UserLogoutView, register, profile
from django.contrib.auth import views as auth_views # Django's built-in auth views
from . import views # Your custom views
from .views import ( # Import specific class-based views for clarity
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

# blog/urls.py




urlpatterns = [
    # --- Authentication URLs ---
    path('register/', views.register, name='register'), # Custom registration view
    # Django's built-in LoginView and LogoutView, using custom templates
    path('login/', auth_views.LoginView.as_as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'), # Custom user profile view
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'), # Changed from 'edit' to 'update'

    # --- Blog Post CRUD URLs ---
    # Home page: lists all blog posts
    path('', PostListView.as_view(), name='post_list'),
    # Create new post
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    # View a single post (uses primary key 'pk' to identify the post)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # Edit an existing post (uses primary key 'pk')
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'), # This is the "update" URL
    # Delete an existing post (uses primary key 'pk')
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]