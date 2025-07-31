from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView  # Import class-based detail view
from .models import Library  # Import the Library model
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
def check_role(role):
     def decorator(user):
        return user.is_authenticated and user.userprofile.role == role
    return user_passes_test(decorator)

@check_role('Admin')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@check_role('Librarian')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@check_role('Member')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in automatically after registration
            return redirect('login')  # Redirect to login page or any other page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


View for user registration
class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
     return render(request, 'relationship_app/register.html', {'form': form})



def list_books(request):
    books = Book.objects.all()  # Get all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})  # Render the book list template

class LibraryDetailView(DetailView):
    model = Library  # Use the Library model
    template_name = 'relationship_app/library_detail.html'  # Template to render
    context_object_name = 'library'  # Name used in the template to refer to the object
