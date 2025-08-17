from django.urls import path
from .views import UserLoginView, UserLogoutView, register, profile

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    # you can add homepage or post list later, e.g., path('', views.home, name='home')
]
